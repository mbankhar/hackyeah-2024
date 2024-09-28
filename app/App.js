import BottomSheet, { BottomSheetTextInput, BottomSheetView } from '@gorhom/bottom-sheet';
import Constants from 'expo-constants';
import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Linking, StyleSheet, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { WebView } from 'react-native-webview';
import { gray } from './colors';

function MapView() {
  const [statusBarHeight, setStatusBarHeight] = useState(0);
  const insets = useSafeAreaInsets();
  const toInputRef = useRef(null);

  useEffect(() => {
    setStatusBarHeight(Constants.statusBarHeight);
  }, []);

  const openStreetMapHtml = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
          * { margin: 0; padding: 0; }
          html, body, #map { height: 100%; width: 100%; }
          #map { background-color: #fbf8f3; }
          .leaflet-control-zoom {
            margin-top: ${statusBarHeight + 16}px !important;
            margin-left: 16px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0px 2px 3.84px rgba(0, 0, 0, 0.25) !important;
          }
          .leaflet-control-zoom-in {
            border-top-left-radius: 8px !important;
            border-top-right-radius: 8px !important;
            border-bottom: 2px solid rgba(0, 0, 0, 0.2) !important;
          }
          .leaflet-control-zoom-out {
            border-bottom-left-radius: 8px !important;
            border-bottom-right-radius: 8px !important;
          }
          .leaflet-control-attribution {
            margin-bottom: calc(20vh + 8px) !important;
            margin-right: ${insets.right}px !important;
          }
          .leaflet-routing-container {
            display: none !important;
          }
        </style>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js"></script>
      </head>
      <body>
        <div id="map"></div>
        <script>
          var map = L.map('map', {
            zoomControl: false,
            attributionControl: false
          }).setView([50.0647, 19.9450], 13); // Krakow

          L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
          }).addTo(map);

          L.control.zoom({
            position: 'topleft'
          }).addTo(map);

          L.control.attribution({
            position: 'bottomright'
          }).addTo(map);

          // Create a custom line style
          var routeStyle = {
            color: 'black',
            weight: 4,
            opacity: 0.8
          };

          // Create custom black marker icons
          var blackIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
          });

          L.Routing.control({
            waypoints: [
              L.latLng(50.0647, 19.9450),  // Example start point
              L.latLng(50.0614, 19.9372)   // Example end point
            ],
            routeWhileDragging: true,
            lineOptions: {
              styles: [routeStyle],
            },
            createMarker: function(i, waypoint, n) {
              return L.marker(waypoint.latLng, {
                icon: blackIcon
              });
            }
          }).addTo(map);
        </script>
      </body>
    </html>
  `;

  const handleExternalLinks = (request) => {
    if (request.url.startsWith('http://') || request.url.startsWith('https://')) {
      Linking.openURL(request.url);
      return false; // Prevent WebView from loading the URL
    }
    return true; // Allow WebView to load the URL
  };

  const bottomSheetRef = useRef(null);

  const snapPoints = useMemo(() => ['20%', '50%'], []);

  const bottomSheetBackgroundStyle = useMemo(() => ({
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    backgroundColor: "white",
    borderRadius: "32px",
    padding: "32px"
  }), []);

  const bottomSheetHandleStyle = useMemo(() => ({
    backgroundColor: null,
  }), []);

  const bottomSheetHandleIndicatorStyle = useMemo(() => ({
    backgroundColor: gray[300],
    width: 32
  }), []);

  const [textFrom, onChangeTextFrom] = useState('');
  const [textTo, onChangeTextTo] = useState('');
  const [showFromInput, setShowFromInput] = useState(false);

  const handleToInputFocus = () => {
    setShowFromInput(true);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="auto" />

      <WebView
        originWhitelist={['*']}
        source={{ html: openStreetMapHtml }}
        style={styles.webView}
        onShouldStartLoadWithRequest={handleExternalLinks}
      />

      <BottomSheet
        ref={bottomSheetRef}
        index={0}
        snapPoints={snapPoints}
        backgroundStyle={bottomSheetBackgroundStyle}
        handleStyle={bottomSheetHandleStyle}
        handleIndicatorStyle={bottomSheetHandleIndicatorStyle}
      >
        <BottomSheetView style={styles.containerBottomSheet}>
          {showFromInput && (
            <BottomSheetTextInput
              onChangeText={onChangeTextFrom}
              value={textFrom}
              placeholder="From where?"
              placeholderTextColor={gray[500]}
              returnKeyType="next"
              onSubmitEditing={() => toInputRef.current?.focus()}
              style={{
                height: "32px",
                width: "80%",
                padding: 16,
                borderRadius: "8px",
                backgroundColor: gray[100],
                fontWeight: "500",
                fontSize: "16px",
                marginBottom: 8
              }}
            />
          )}

          <BottomSheetTextInput
            ref={toInputRef}
            onChangeText={onChangeTextTo}
            value={textTo}
            placeholder="Where to?"
            placeholderTextColor={gray[500]}
            returnKeyType="send"
            onFocus={handleToInputFocus}
            style={{
              height: "32px",
              width: "80%",
              padding: 16,
              borderRadius: "8px",
              backgroundColor: gray[100],
              fontWeight: "500",
              fontSize: "16px"
            }}
          />
        </BottomSheetView>
      </BottomSheet>
    </View>
  );
}

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <MapView />
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  webView: {
    flex: 1,
  },
  containerBottomSheet: {
    flex: 1,
    alignItems: 'center',
  }
});
