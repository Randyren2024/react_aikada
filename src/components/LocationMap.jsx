import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

const LocationMap = ({ lat, lng, accuracy = null, className = '' }) => {
  const mapRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const DefaultIcon = L.icon({
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    L.Marker.prototype.options.icon = DefaultIcon;
    const map = L.map(containerRef.current, {
      zoomControl: false,
    }).setView([lat, lng], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: ''
    }).addTo(map);
    const marker = L.marker([lat, lng]).addTo(map);
    if (accuracy && accuracy > 0) {
      L.circle([lat, lng], { radius: accuracy, color: '#22c55e', weight: 1, fillOpacity: 0.1 }).addTo(map);
    }
    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [lat, lng, accuracy]);

  return <div ref={containerRef} className={className} style={{ height: '160px', borderRadius: '0.75rem', overflow: 'hidden' }} />;
};

export default LocationMap;
