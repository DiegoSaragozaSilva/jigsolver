// src/components/Header/Header.tsx
import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            alignItems: "center",
            justifyContent: "center",
            display: "flex",
            flexDirection: "row",
          }}
        >
          JigSolver
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
