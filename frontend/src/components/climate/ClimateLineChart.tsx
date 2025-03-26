"use client";

import { HStack } from "@chakra-ui/react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import React, { use, useEffect, useState } from "react";
// @ts-ignore
import { Line } from "react-chartjs-2";

import { Temperature, Humidity } from "@/types";

interface Props {
  temperature: Temperature[];
  humidity: Humidity[];
}

interface Dataset {
  label: string;
  data: number[];
  borderColor: string;
  backgroundColor: string;
}

interface Data {
  labels: string[];
  datasets: Dataset[];
}

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Climate Chart",
    },
  },
};

export default function ClimateLineChart({ temperature, humidity }: Props) {
  const [data, setData] = useState<Data>({
    labels: [],
    datasets: [],
  });

  useEffect(() => {
    const labels = [];
    const datasets: Dataset[] = [];
    for (
      let index = 0;
      index < Math.max(temperature.length, humidity.length);
      index++
    ) {
      const count =
        temperature.length > index && humidity.length > index ? 2 : 1;
      const avgDate = new Date(
        (temperature[index]?.created_at_timestamp ||
          0 + humidity[index]?.created_at_timestamp ||
          0) / count,
      );
      labels.push(`${avgDate.getHours()}:${avgDate.getMinutes()}`);
    }

    if (temperature.length > 0) {
      datasets.push({
        label: "Temperature",
        data: temperature.map((t) => t.temperature),
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      });
    }
    if (humidity.length > 0) {
      datasets.push({
        label: "Humidity",
        data: humidity.map((h) => h.humidity),
        borderColor: "rgb(53, 162, 235)",
        backgroundColor: "rgba(53, 162, 235, 0.5)",
      });
    }

    setData({
      labels,
      datasets,
    });
  }, [temperature, humidity]);

  return (
    <HStack w='100%' h='100%'>
      <Line options={options} data={data} />
    </HStack>
  );
}
