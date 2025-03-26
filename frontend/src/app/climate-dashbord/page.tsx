'use client';

import { Grid, HStack, Stack, Text, VStack } from "@chakra-ui/react";

import ClimateLineChart from "@/components/climate/ClimateLineChart";
import GaugeClimate from "@/components/climate/GaugeClimate";
import { useQuery } from "@tanstack/react-query";
import { getTemperature, getCurrentTemperature } from "@/api/temperature";
import { useEffect, useState } from "react";
import { Temperature } from "@/types/temperature";

export default function Page() {

  const [temperature, setTemperature] = useState<Temperature[]>([]);
  const [currentTemperature, setCurrentTemperature] = useState<Temperature>();

  const { data: temperatureData, isError: temperatureError } = useQuery({
    queryKey: ["temperature"],
    queryFn: () => getTemperature({
      start_timestamp: Math.trunc(new Date().setHours(0, 0, 0, 0)),
      end_timestamp: Math.trunc(new Date().setHours(23, 59, 59)),
    }),
  });

  const { data: currentTemperatureData, isError: currentTemperatureError } = useQuery({
    queryKey: ["currentTemperature"],
    queryFn: () => getCurrentTemperature(),
  });

  useEffect(() => {
    if (temperatureError) {
      console.log(temperatureError);
    }
    if (temperatureData) {
      setTemperature(temperatureData.data);
    }

  }, [temperatureData, temperatureError]);

  useEffect(() => {
    if (currentTemperatureError) {
      console.log(currentTemperatureError);
    }
    if (currentTemperatureData) {
      setCurrentTemperature(currentTemperatureData.data);
    }
  })
  return (
    <Grid
      templateColumns={{
        base: "repeat(2, 1fr)",
        md: "repeat(4, 1fr)",
        lg: "repeat(6, 1fr)",
      }}
      templateRows={{
        base: "repeat(8, 1fr)",
        md: "repeat(6, 1fr)",
        lg: "repeat(4, 1fr)",
      }}
      gap={4}
      w="100%"
      h="100%"
      flexGrow={1}
    >
      <Stack
        gridColumn={{
          base: "1 / span 2",
          md: "1 / span 2",
          lg: "1 / span 2",
        }}
        gridRow={{
          base: "1 / span 2",
          md: "1 / span 2",
          lg: "1 / span 2",
        }}
      >
        <GaugeClimate value={currentTemperature?.temperature || 0} units={"°C"} minValue={10} maxValue={40} />
      </Stack>

      <Stack
        gridColumn={{
          base: "1 / span 2",
          md: "3 / span 2",
          lg: "3 / span 2",
        }}
        gridRow={{
          base: "3 / span 2",
          md: "1 / span 2",
          lg: "1 / span 2",
        }}
      >
        <GaugeClimate
          value={15}
          units={"%"}
          subArcs={[{ color: "rgb(53, 162, 235)" }]}
        />
      </Stack>

      <VStack
        gridColumn="1 / span 1"
        justifyContent="center"
        alignItems="center"
      >
        <Text>Daily Avg Temperature:</Text>
        <HStack>15°C</HStack>
      </VStack>
      <VStack justifyContent="center" alignItems="center">
        <Text>Daily Avg Humidity:</Text>
        <HStack>15%</HStack>
      </VStack>

      <Stack
        gridColumn={{
          base: "1 / span 2",
          md: "3 / span 2",
          lg: "4 / span 3",
        }}
        gridRow={{
          base: "4 / span 4",
          md: "2 / span 2",
          lg: "3 / span 2",
        }}
      >
        <ClimateLineChart
          temperature={temperature}
          humidity={[{ humidity: 15, created_at_timestamp: 1 }]}
        />
      </Stack>
    </Grid>
  );
}
