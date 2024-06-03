import React from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import Typography from "@mui/material/Typography";

interface SliderControlProps {
  label: string;
  value: number;
  onChange: (newValue: number) => void;
}

const SliderControl: React.FC<SliderControlProps> = ({
  label,
  value,
  onChange,
}) => {
  const handleChange = (event: Event, newValue: number | number[]) => {
    onChange(newValue as number);
  };

  return (
    <Box sx={{ width: 300, padding: 2 }}>
      <Typography id="input-slider" gutterBottom>
        {label}
      </Typography>
      <Slider
        value={value}
        onChange={handleChange}
        aria-labelledby="input-slider"
        min={50}
        max={300}
        valueLabelDisplay="auto"
      />
    </Box>
  );
};

export default SliderControl;
