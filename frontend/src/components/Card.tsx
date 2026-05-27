import React, { ReactNode } from "react";
import { motion } from "framer-motion";

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

const Card: React.FC<CardProps> = ({ children, className = "", hover = true }) => {
  return (
    <motion.div
      className={`glass-dark p-6 rounded-lg ${hover ? "hover:bg-slate-800/60 cursor-pointer" : ""} ${className}`}
      whileHover={hover ? { scale: 1.02 } : {}}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
};

export default Card;
