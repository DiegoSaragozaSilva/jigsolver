import React, { ReactNode } from "react";
import { useTheme } from "@mui/material/styles";

interface SectionWrapperProps {
  children: ReactNode;
  flexDirection?: "column" | "row";
  alignItems?: "center" | "flex-start" | "flex-end";
  marginTop?: string;
  gap?: string;
}

const SectionWrapper: React.FC<SectionWrapperProps> = ({
  children,
  flexDirection = "column",
  alignItems = "center",
  marginTop = "0%",
  gap = "0%",
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
        marginTop: marginTop,
        gap: gap,
      }}
    >
      {children}
    </div>
  );
};

export default SectionWrapper;
