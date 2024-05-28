import React, { ReactNode } from "react";
import { useTheme } from "@mui/material/styles";

interface SectionWrapperProps {
  children: ReactNode;
  flexDirection?: "column" | "row";
  alignItems?: "center" | "flex-start" | "flex-end";
}

const SectionWrapper: React.FC<SectionWrapperProps> = ({
  children,
  flexDirection = "column",
  alignItems = "center",
}) => {
  const theme = useTheme();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: flexDirection,
        justifyContent: "center",
        alignItems: alignItems,
        width: "100%",
        height: "100%",
        color: theme.palette.text.secondary,
      }}
    >
      {children}
    </div>
  );
};

export default SectionWrapper;
