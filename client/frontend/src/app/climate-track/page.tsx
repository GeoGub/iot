'use client';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { useQuery } from '@tanstack/react-query';
import { getTemperature } from '@/api/temperature';
import { useEffect, useRef, useState } from 'react';
import { Temperature } from '@/types';

// Подключаем адаптер для работы с датами
import 'chartjs-adapter-date-fns';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler, Legend, TimeScale);

// Динамическая загрузка chartjs-plugin-zoom
if (typeof window !== 'undefined') {
  import('chartjs-plugin-zoom').then((zoomPlugin) => {
    ChartJS.register(zoomPlugin.default);
  });
}

interface GraphPoint {
  x: Date;
  y: number;
}

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Temperature Chart with Zoom',
    },
    zoom: {
      pan: {
        enabled: true,
        mode: 'x' as 'x', // Исправлено
      },
      zoom: {
        wheel: {
          enabled: true,
        },
        mode: 'x' as 'x', // Исправлено
      },
      onZoomComplete: ({chart}) => {
        console.log(chart)
      }
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
        },
        ticks: {
          // Установите интервал, чтобы избежать переполнения временных меток
          autoSkip: true,
          maxTicksLimit: 10,  // Ограничьте количество меток
        },
      },
      y: {
        beginAtZero: false,
        suggestedMin: 0,  // Подсказка для минимального значения
        suggestedMax: 50, // Подсказка для максимального значения
        ticks: {
          stepSize: 0.5, // Это можно адаптировать в зависимости от данных
        },
      },
    },
  },
};

export default function Page() {
  const chartRef = useRef<ChartJS<'line'> | null>(null);
  const [dataTemperatures, setDataTemperatures] = useState({
    labels: [],
    datasets: [
      {
        fill: true,
        label: 'Temperature',
        data: [],
        borderColor: 'rgb(53, 162, 235)',
        // backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  });

  const { data, error, isLoading } = useQuery({
    queryKey: ['temperature'],
    queryFn: getTemperature,
    refetchInterval: 10000,
  });

  useEffect(() => {
    if (data?.data?.items) {
      const temperatures = data.data.items.map((item: Temperature) => ({
        x: new Date(item.created_at_timestamp * 1000).toLocaleString(),
        y: item.temperature,
      }));

      setDataTemperatures({
        labels: temperatures.map((t: GraphPoint) => t.x),
        datasets: [
          {
            ...dataTemperatures.datasets[0],
            data: temperatures.map((t: GraphPoint) => t.y),
          },
        ],
      });
    }
  }, [data]);

  const onResetZoom = () => {
    if (!chartRef.current) return;
    chartRef.current.resetZoom();
  };

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading data</p>;

  return (
    <div>
      <h1>Climate Track</h1>
      <Line ref={chartRef} options={options} data={dataTemperatures} />
      <button onClick={onResetZoom}>Reset Zoom</button>
    </div>
  );
}
