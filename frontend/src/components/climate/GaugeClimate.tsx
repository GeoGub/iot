"use client";

import { HStack } from "@chakra-ui/react";
import GaugeComponent from "react-gauge-component";

type Tick = {
  value: number;
};

type SubArc = {
  limit?: number;
  color: string;
  showTick?: boolean;
  tooltip?: {
    text: string;
  };
  onClick?: () => void;
  onMouseMove?: () => void;
  onMouseLeave?: () => void;
};

interface Props {
  value: number;
  units: string;
  minValue?: number;
  maxValue?: number;
  ticks?: Tick[];
  subArcs?: SubArc[];
  fontSize?: number;
}

// [
//   {
//     limit: 15,
//     color: "#EA4228",
//     showTick: true,
//     tooltip: {
//       text: "Too low temperature!",
//     },
//     onClick: () => console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
//     onMouseMove: () => console.log("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"),
//     onMouseLeave: () => console.log("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"),
//   },
//   {
//     limit: 17,
//     color: "#F5CD19",
//     showTick: true,
//     tooltip: {
//       text: "Low temperature!",
//     },
//   },
//   {
//     limit: 28,
//     color: "#5BE12C",
//     showTick: true,
//     tooltip: {
//       text: "OK temperature!",
//     },
//   },
//   {
//     limit: 30,
//     color: "#F5CD19",
//     showTick: true,
//     tooltip: {
//       text: "High temperature!",
//     },
//   },
//   {
//     color: "#EA4228",
//     tooltip: {
//       text: "Too high temperature!",
//     },
//   },
// ],

export default function GaugeClimate({
  value,
  units,
  ticks,
  subArcs,
  fontSize = 10,
  minValue = 0,
  maxValue = 100,
}: Props) {
  return (
    <HStack p={1} w="100%" h="100%" justifyContent="center" alignItems="center">
      <GaugeComponent
        type="semicircle"
        arc={{
          width: 0.15,
          padding: 0.005,
          cornerRadius: 1,
          // gradient: true,
          subArcs: subArcs || [{ color: "red" }],
        }}
        pointer={{
          color: "#345243",
          length: 0.8,
          width: 15,
          // elastic: true,
        }}
        labels={{
          valueLabel: { formatTextValue: (value) => value + units },
          tickLabels: {
            type: "outer",
            defaultTickValueConfig: {
              formatTextValue: (value: number) => value + units,
              style: { fontSize: fontSize },
            },
            ticks:
              ticks ||
              Array.from(
                { length: Math.floor((maxValue - minValue) / 10) + 1 },
                (_, i) => ({ value: minValue + i * 10 }),
              ),
          },
        }}
        value={value}
        minValue={minValue}
        maxValue={maxValue}
      />
    </HStack>
  );
}
