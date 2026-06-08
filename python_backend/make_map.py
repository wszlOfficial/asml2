from shapely.geometry import Point
from shapely import box
from shapely.ops import voronoi_diagram
import geopandas as gpd


class MapGenerator():
    '''Generates a HTML map containing datapoints'''
    def __init__(self, df):
        self.df = df
        self.min_lon = df['longlitude'].min()
        self.max_lon = df['longlitude'].max()
        self.min_lat = df['latitude'].min()
        self.max_lat = df['latitude'].max()


    def points_to_fields(self, grouped_parameter):
        '''Turns GPS coordinates into a field of Voronoi shapes'''
        df = self.df
        self.grouped_parameter = grouped_parameter

        geometry = [Point(xy) for xy in zip(df['longlitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

        # Turn points into voronoi shapes
        all_points = gdf.geometry.union_all()
        buffer = 0.001
        bbox = box(
            self.min_lon - buffer,
            self.min_lat - buffer,
            self.max_lon + buffer,
            self.max_lat + buffer,
        )
        gdf_bbox = gpd.GeoDataFrame(geometry=[bbox], crs='EPSG:4326')   
        voronoi_polys = voronoi_diagram(all_points, envelope=bbox)

        # New dataframe with the voronoi shapes
        gdf_voronoi = gpd.GeoDataFrame(geometry=list(voronoi_polys.geoms), crs='EPSG:4326')
        
        gdf_voronoi_clipped = gpd.clip(gdf_voronoi, gdf_bbox)  # Clip all shapes outside of the bounding box
        self.gdf_fields = gpd.sjoin(gdf_voronoi_clipped, gdf, how="inner", predicate="intersects")
        return self.gdf_fields
    

    def save_map(self, cmap, categorical=True):
        '''Exports an interactive map to be embedded onto the website'''
        return self.gdf_fields.explore(
                                categorical=categorical,
                                column=self.grouped_parameter,
                                cmap=cmap, 
                                tiles="CartoDB positron",  # CartoDB is free-to-use and open source
                                style_kwds=dict(
                                    fillOpacity=0.6,   # Makes the fields slightly transparent
                                    weight=0
                                )
    )
        

class Map():  # Small data structure to save what should be in the maps.
    def __init__(self, datapoint: str, filename: str, cmap: str, *, categorical=True):
        self.datapoint = datapoint
        self.filename = filename
        self.cmap = cmap
        self.categorical = categorical