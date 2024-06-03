// src/theme.ts
import { createTheme } from "@mui/material/styles";

const draculaTheme = createTheme({
  palette: {
    primary: {
      main: "#bd93f9", // purple
    },
    secondary: {
      main: "#ff79c6", // pink
    },
    error: {
      main: "#ff5555", // red
    },
    background: {
      default: "#282a36", // dark grey
      paper: "#44475a", // light grey
    },
    text: {
      primary: "#f8f8f2", // very light grey
      secondary: "#6272a4", // grey blue
    },
  },

  typography: {
    fontFamily: "Roboto, sans-serif",
    fontSize: 16,
  },
});

export default draculaTheme;
