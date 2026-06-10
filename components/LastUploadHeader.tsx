"use client";

import { useEffect, useState } from "react";

const API_BASE_URL = "https://api.asml2.nl";

type LastUploadResponse = {
  last_upload: string | null;
};

function formatUploadTime(timestamp: string) {
  const date = new Date(timestamp);
  if (isNaN(date.getTime())) return null;

  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSeconds = Math.round(diffMs / 1000);
  const diffMinutes = Math.round(diffSeconds / 60);
  const diffHours = Math.round(diffMinutes / 60);

  if (diffSeconds < 60) {
    return `just now`;
  }
  if (diffMinutes < 60) {
    return `${diffMinutes} minute${diffMinutes === 1 ? "" : "s"} ago`;
  }
  if (diffHours < 24) {
    return `${diffHours} hour${diffHours === 1 ? "" : "s"} ago`;
  }

  return date.toLocaleString();
}

export default function LastUploadHeader() {
  const [text, setText] = useState("Loading last update...");

  useEffect(() => {
    fetch(`${API_BASE_URL}/last-upload`)
      .then((response) => response.json())
      .then((data: LastUploadResponse) => {
        if (data?.last_upload) {
          const formatted = formatUploadTime(data.last_upload);
          setText(
            formatted
              ? `Last API update: ${formatted}`
              : "Last API update: unknown"
          );
        } else {
          setText("Last API update: no upload recorded yet");
        }
      })
      .catch(() => {
        setText("Last API update: unavailable");
      });
  }, []);

  return (
    <p className="text-xs text-slate-500 tracking-tight text-center w-full max-w-5xl mb-3">
      {text}
    </p>
  );
}
