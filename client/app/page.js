"use client"
import { useEffect, useState } from "react";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import axios from "axios";

export default function Home() {
  const [location, setLocation] = useState([35.20472109, -114.0534769]);
  const [radius, setRadius] = useState();
  const [foodTrucks, setFoodTrucks] = useState([]);
  console.log(location, radius, foodTrucks);

  const handleSearch = () => {
    axios.get("http://127.0.0.1:8000/api/foodtruck", {
      params: {
        lat: location[0],
        lon: location[1],
        rad: radius
      }
    }).then((response) => {
      console.log(response.data);
      setFoodTrucks(response.data);
    })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    axios.get("https://ipapi.co/json/").then((response) => {
      console.log(response.data);
      setLocation([response.data.latitude, response.data.longitude]);
    })
      .catch((error) => {
        console.log(error);
      });
  });

  return (
    <main className={styles.main}>
      <h1>Welcome to Food Trucks Quest</h1>
      <br />
      <input value={radius} onChange={(e) => setRadius(e.target.value)} className={styles.searchbox} type="number" placeholder="Enter the Radius (Kilometers)" />
      <Button variant="primary" onClick={handleSearch}>Search</Button>
      <br /><br />
      <div className={styles.cardbox}>
        {foodTrucks.map((foodTruck) => {
          return (
            <span className={styles.card} key={foodTruck.id}>
              <h5>{foodTruck.name}</h5>
              <p>Distance from You: <i>{foodTruck.distance} Kms</i></p>
              <p>{foodTruck.address}</p>
              <p>{foodTruck.fooditems}</p>
            </span>
          );
        })}
      </div>
    </main>
  );
}
