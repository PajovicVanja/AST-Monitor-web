<script setup lang="ts">
import { onMounted, ref } from 'vue';
import RouteProgress from './components/RouteProgress.vue';
import Map from './components/Map.vue';
import DisplayCard from './components/DisplayCard.vue';
import type { LatLngExpression } from 'leaflet';
import TrainingMetrics from './components/TrainingMetrics.vue';
import axios from 'axios';

const progress = ref(0);
const remainingDistance = ref(0);
const speed = ref<number | undefined>(undefined);
const lastValidSpeed = ref<number | undefined>(undefined);
const heartrate = ref(0);
const duration = ref('00:00:00');
const distance = ref(0);
const mapRef = ref([46.4217242, 15.8731548] as LatLngExpression);
const ascent = ref(5);
const remainingAscent = ref(0);
const routeInput = ref([]);
const speeds = ref<number[]>([]);

function setValues(newValues: {
  progress?: number,
  remainingDistance?: number,
  remainingAscent?: number,
  speed?: number,
  heartrate?: number,
  duration?: string,
  distance?: number;
  lat_lng?: LatLngExpression;
  ascent?: number;
  routeInput?: [];
}) {
  if (newValues.progress !== undefined) progress.value = newValues.progress;
  if (newValues.remainingDistance !== undefined) remainingDistance.value = newValues.remainingDistance;
  if (newValues.remainingAscent !== undefined) remainingAscent.value = newValues.remainingAscent;
  if (newValues.speed !== undefined) {
    speed.value = newValues.speed;
    if (newValues.speed !== null) {
      lastValidSpeed.value = newValues.speed;
      speeds.value.push(newValues.speed);
    }
  } else if (lastValidSpeed.value !== undefined) {
    speed.value = lastValidSpeed.value;
  }
  if (newValues.heartrate !== undefined) heartrate.value = newValues.heartrate;
  if (newValues.duration !== undefined) duration.value = newValues.duration;
  if (newValues.distance !== undefined) distance.value = newValues.distance;
  if (newValues.lat_lng !== undefined) {
    console.log('Received lat_lng:', newValues.lat_lng);
    mapRef.value = newValues.lat_lng;
  }
  if (newValues.ascent !== undefined) ascent.value = newValues.ascent;
  if (newValues.routeInput !== undefined) routeInput.value = newValues.routeInput;
}

async function fetchLatestData() {
  try {
    console.log('Fetching latest data...');
    const response = await axios.get('http://localhost:5000/sensor/api/latest-data');
    const data = response.data;
    console.log('Received data:', data);
    console.log('Received speed:', data.speed);

    setValues({
      progress: data.progress,
      remainingDistance: data.remainingDistance,
      remainingAscent: data.remainingAscent,
      speed: data.speed !== null ? data.speed : undefined,
      heartrate: Number(data.heartrate),
      duration: data.duration,
      distance: data.distance,
      lat_lng: data.lat_lng ? [data.lat_lng[0], data.lat_lng[1]] as LatLngExpression : mapRef.value,
      ascent: data.ascent,
      routeInput: data.route?.route_render?.map((point: any) => ({ lat: point.lat, lon: point.lon })) || []
    });

    // Send data to a new route for later saving
    await axios.post('http://localhost:5000/sensor/api/temp-training-data', data);
  } catch (error) {
    console.error('Error fetching latest data:', error);
  }
}

async function fetchRoute() {
  try {
    console.log('Fetching route data...');
    const response = await axios.get('http://localhost:5000/sensor/api/route');
    const data = response.data;
    console.log('Received route data:', data);
    // Logic for drawing the route on the map has been removed
  } catch (error) {
    console.error('Error fetching route data:', error);
  }
}

onMounted(() => {
  let w = window as unknown as CustomWindow;
  w.setValues = setValues;

  fetchRoute();
  setInterval(fetchLatestData, 3000);
});

export interface CustomWindow extends Window {
  setValues: any;
}
</script>

<template>
  <div class="row m-0 text-center" style="height: 84vh; background-color: rgb(254, 254, 254);">
    <div class="col-10 p-0">
      <Map :route-input="routeInput" :marker-lat-lng="mapRef"></Map>
    </div>
    <div class="col-2 pl-2 ">
      <RouteProgress :progress="progress" :remaining-distance="remainingDistance" :remaining-ascent="remainingAscent">
      </RouteProgress>
    </div>
  </div>
  <div class="row m-0 align-items-center p-0" style="height: 15vh;">
    <TrainingMetrics :speed="speed" :ascent="ascent" :heartrate="heartrate" :distance="distance" :duration="duration">
    </TrainingMetrics>
  </div>
</template>

<style scoped></style>
