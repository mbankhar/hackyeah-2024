import Feather from '@expo/vector-icons/Feather';
import BottomSheet, { BottomSheetTextInput, BottomSheetView } from '@gorhom/bottom-sheet';
import Constants from 'expo-constants';
import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useMemo, useRef, useState } from 'react';
<<<<<<< HEAD
import { Linking, StyleSheet, View } from 'react-native';
=======
import { ActivityIndicator, Linking, Modal, SafeAreaView, ScrollView, StyleSheet, Switch, Text, TouchableOpacity, View } from 'react-native';
>>>>>>> d0a944c... (app) implement settings drawer
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { WebView } from 'react-native-webview';
import { gray } from './colors';

const Condition = ({ text }) => {
  const [isEnabled, setIsEnabled] = useState(true);
  const toggleSwitch = () => setIsEnabled(previousState => !previousState);

  return (
    <View
      style={{
        width: "100%",
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 8
      }}
    >
      <Switch
        trackColor={{ true: '#410ff8' }}
        onValueChange={toggleSwitch}
        value={isEnabled}
        style={{
          marginRight: 8
        }}
      />

      <Text style={{ fontWeight: "semibold", flex: 1 }}>
        {text}
      </Text>
    </View>
  )
}

const Menu = ({ isVisible, onClose }) => {
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={isVisible}
      onRequestClose={onClose}
    >
      <SafeAreaView style={styles.menuContainer}>
        <View style={styles.menuContent}>
          <ScrollView contentContainerStyle={styles.menuScrollContent}>
            <Text style={styles.menuTitle}>Settings</Text>

            <Text
              style={{
                marginTop: 8,
                color: gray[500],
                textAlign: "center",
                marginBottom: 32
              }}
            >
              Your conditions for a safe route.
            </Text>

            <Condition
              text="Avoid unlit roads during night hours"
            />
            <Condition
              text="Prioritize paved and asphalt surfaces"
            />
            <Condition
              text="Prioritize roads with dedicated cycleways"
            />
            <Condition
              text="Prefer smooth roads (excellent/good surface quality)"
            />
            <Condition
              text="Avoid routes with a history of traffic incidents"
            />
            <Condition
              text="Avoid roads with high real-time traffic"
            />
            <Condition
              text="Avoid roads with poor surface quality"
            />
            <Condition
              text="Avoid roads under construction"
            />
            <Condition
              text="Favor wide roads (greater than 5 meters)"
            />
            <Condition
              text="Avoid roads with parking lanes during busy hours"
            />

            <TouchableOpacity
              onPress={onClose}
              style={{
                height: "32px",
                width: "80%",
                padding: 16,
                borderRadius: "8px",
                backgroundColor: "#410ff8",
                marginTop: 32,
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Text
                  style={{
                    fontWeight: "500",
                    fontSize: "16px",
                    color: "white"
                  }}
                >
                  Save
                </Text>
            </TouchableOpacity>
          </ScrollView>
        </View>
      </SafeAreaView>
    </Modal>
  );
};

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

<<<<<<< HEAD
=======
  const handleSubmit = () => {
    calculateRoute();
  };
  
  const [isMenuVisible, setIsMenuVisible] = useState(false);

  const toggleMenu = () => {
    setIsMenuVisible(!isMenuVisible);
  };

  const IconButton = () => (
    <TouchableOpacity
      style={styles.iconButton}
      onPress={toggleMenu}
    >
      <Feather name="menu" size={24} color="black" />
    </TouchableOpacity>
  );

>>>>>>> d0a944c... (app) implement settings drawer
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

      <IconButton />
      <Menu isVisible={isMenuVisible} onClose={() => setIsMenuVisible(false)} />
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
  },
  iconButton: {
    position: 'absolute',
    top: Constants.statusBarHeight + 16,
    right: 16,
    backgroundColor: 'white',
    borderRadius: 999,
    width: 48,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    zIndex: 1,
  },
  menuContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0, 0, 0, 0.5)'
  },
  menuContent: {
    backgroundColor: 'white',
    borderTopLeftRadius: 32,
    borderTopRightRadius: 32,
    maxHeight: '80%',
  },
  menuScrollContent: {
    padding: 24,
    alignItems: "center"
  },
  menuTitle: {
    fontSize: 24,
    fontWeight: 'bold'
  },
  menuItem: {
    padding: 10,
  },
});
