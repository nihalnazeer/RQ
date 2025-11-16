"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function WelcomeSplash({
  name = "Mr. Aashiq",
}: {
  name?: string;
}) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(false), 2600);
    return () => clearTimeout(timer);
  }, []);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8 }}
          className="fixed inset-0 flex items-center justify-center bg-[#0E0F11] z-[9999]"
        >
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="text-center"
          >
            <h1 className="text-3xl md:text-4xl font-light tracking-wide text-white">
              Welcome, <span className="font-normal">{name}</span>
            </h1>

            <p className="text-sm md:text-base text-neutral-400 mt-3 tracking-wide">
              Preparing your operational insights…
            </p>

            {/* Subtle thin line */}
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "130px" }}
              transition={{ duration: 1.2, ease: "easeInOut", delay: 0.3 }}
              className="h-[1px] bg-neutral-700 mx-auto mt-6"
            />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
