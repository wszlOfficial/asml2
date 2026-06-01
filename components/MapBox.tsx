interface MapBoxProps {
  filename?: string;
  title?: string;
}

export default function MapBox({ 
  filename = "testmap.html", 
  title = "Spatial Data Distribution Map" 
}: MapBoxProps) {
  
  return (
    // We change the layout to a flex column that scales beautifully
    <div className="flex flex-col items-center w-full h-full min-h-0">
      {/* Title - responsive text sizing so it doesn't crowd out the map on mobile */}
      <h2 className="text-sm md:text-base font-bold mb-2 text-gray-850 text-center shrink-0 truncate w-full px-2">
        {title}
      </h2>
      
      {/* THE DYNAMIC SQUARE FIX: 
        - w-full aspect-square lets it be a square based on width by default.
        - h-full max-h-[32dvh] md:max-h-[55dvh] acts as a ceiling. If the screen is too short, 
          the map shrinks vertically, and aspect-square forces the width to shrink along with it!
      */}
      <div className="relative w-full aspect-square h-full max-h-[32dvh] md:max-h-[55dvh] rounded-xl overflow-hidden border border-gray-200 shadow-lg bg-gray-50 shrink min-h-0">
        <iframe
          src={`/${filename}`}
          title={title}
          className="absolute top-0 left-0 w-full h-full border-0"
          allowFullScreen
        />
      </div>
    </div>
  );
}