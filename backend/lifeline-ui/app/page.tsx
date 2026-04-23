"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export default function Page() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [ambulancePos, setAmbulancePos] = useState(0);
  const [emergency, setEmergency] = useState("accident");

  // 📍 Trigger Emergency
  const handleEmergency = async () => {
    setLoading(true);

    navigator.geolocation.getCurrentPosition(async (pos) => {
      const res = await fetch("http://127.0.0.1:8000/emergency", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          location: {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
          },
          emergency: emergency,
        }),
      });

      const data = await res.json();
      setResult(data.response);
      setAmbulancePos(0);
      setLoading(false);
    });
  };

  // 🚑 Animate ambulance
  useEffect(() => {
    if (!result) return;

    const interval = setInterval(() => {
      setAmbulancePos((prev) => (prev >= 100 ? 100 : prev + 2));
    }, 150);

    return () => clearInterval(interval);
  }, [result]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-red-900 text-white flex flex-col items-center justify-center p-6">

      {/* 🚑 Title */}
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-5xl font-bold mb-6"
      >
        🚑 LifeLine AI
      </motion.h1>

      {/* 🚨 Emergency Type Selector */}
      <div className="flex gap-3 mb-4">
        {["accident", "heart", "injury"].map((type) => (
          <button
            key={type}
            onClick={() => setEmergency(type)}
            className={`px-4 py-2 rounded-lg ${
              emergency === type ? "bg-red-500" : "bg-gray-700"
            }`}
          >
            {type.toUpperCase()}
          </button>
        ))}
      </div>

      {/* 🚨 Trigger Button */}
      <button
        onClick={handleEmergency}
        className="bg-red-500 px-6 py-3 rounded-xl text-lg animate-pulse"
      >
        {loading ? "Processing..." : "🚨 Trigger Emergency"}
      </button>

      {/* 📊 RESULT PANEL */}
      {result && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8 w-full max-w-md backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 shadow-xl"
        >
          <p><strong>🏥 Hospital:</strong> {result.hospital}</p>
          <p><strong>🚑 Ambulance:</strong> {result.ambulance}</p>

          {/* ⚡ Priority Badge */}
          <p>
            <strong>⚡ Priority:</strong>{" "}
            <span
              className={`px-2 py-1 rounded ${
                result.priority === "HIGH"
                  ? "bg-red-500"
                  : "bg-yellow-500"
              }`}
            >
              {result.priority}
            </span>
          </p>

          <p><strong>⏱ ETA:</strong> {result.eta}</p>
          <p><strong>📏 Distance:</strong> {result.distance_km} km</p>

          {/* 🚑 Tracking Bar */}
          <div className="mt-4 w-full bg-gray-700 rounded-full h-6 overflow-hidden">
            <motion.div
              className="h-6 bg-green-500 flex items-center justify-end pr-2 text-sm"
              style={{ width: `${ambulancePos}%` }}
            >
              🚑
            </motion.div>
          </div>

          <p className="text-center mt-2">
            Ambulance arriving... {ambulancePos}%
          </p>

          {/* 🌍 Map */}
          <iframe
            src={`https://www.google.com/maps?q=${result.location.lat},${result.location.lng}&z=15&output=embed`}
            className="w-full h-40 mt-4 rounded-xl"
          />

          {/* 📍 Open Maps */}
          <a href={result.map} target="_blank">
            <button className="mt-4 w-full bg-blue-500 py-2 rounded-lg">
              Open in Maps
            </button>
          </a>
        </motion.div>
      )}
    </div>
  );
}