import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion"; // ✅ Tambahan untuk animasi
import autos from "../assets/bg/asas/autoscan.png";
import keyabout from "../assets/bg/asas/keyabout.png";
import uploadapk from "../assets/bg/asas/uploadapk.png";
import result from "../assets/bg/asas/result.png";
import images from "../assets/bg/bg.png";
import globe from "../assets/bg/globe.png";
import worlda from "../assets/bg/world.png";

// 🔹 Navbar Component
const Navbar = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 w-full bg-[#071235]/80 backdrop-blur-md text-white flex items-center justify-between px-6 md:px-8 py-4 shadow-lg z-50">
      <div className="flex items-center space-x-3">
        <img src={worlda} alt="APK Trust Logo" className="w-10 h-10" />
        <span className="font-bold text-lg tracking-wide">APK TRUST</span>
      </div>

      <div className="hidden md:flex items-center space-x-8 border border-white/60 rounded-lg px-6 py-2 shadow-md">
        <a href="#home" className="hover:text-[#5380ea] font-semibold">Home</a>
        <a href="#about" className="hover:text-[#5380ea] font-semibold">About</a>
        <a href="#faq" className="hover:text-[#5380ea] font-semibold">FAQ</a>
        <a href="#contact" className="hover:text-[#5380ea] font-semibold">Contact</a>
      </div>

      <button
        onClick={() => navigate("/upload")}
        className="hidden md:block bg-[#5380ea] hover:bg-[#3c6ff7] transition-all text-white font-semibold px-6 py-2 rounded-full shadow-md"
      >
        Upload APK
      </button>

      {/* Menu Mobile */}
      <div className="md:hidden flex items-center">
        <button
          className="text-white text-2xl focus:outline-none"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? "✖" : "☰"}
        </button>
      </div>

      {isOpen && (
        <div className="absolute top-16 left-0 w-full bg-[#071235] text-center flex flex-col space-y-4 py-6 border-t border-white/20 md:hidden">
          <a href="#home" onClick={() => setIsOpen(false)} className="hover:text-[#5380ea] font-semibold">Home</a>
          <a href="#about" onClick={() => setIsOpen(false)} className="hover:text-[#5380ea] font-semibold">About</a>
          <a href="#faq" onClick={() => setIsOpen(false)} className="hover:text-[#5380ea] font-semibold">FAQ</a>
          <a href="#contact" onClick={() => setIsOpen(false)} className="hover:text-[#5380ea] font-semibold">Contact</a>
          <button
            onClick={() => {
              navigate("/upload");
              setIsOpen(false);
            }}
            className="bg-[#5380ea] hover:bg-[#3c6ff7] transition-all text-white font-semibold mx-20 py-2 rounded-full shadow-md"
          >
            Upload APK
          </button>
        </div>
      )}
    </nav>
  );
};

// 🔹 Home Component
const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="bg-white w-full min-h-screen flex flex-col text-gray-800 scroll-smooth">
      <Navbar />

      {/* HERO SECTION */}
      <section
        id="home"
        style={{
          backgroundImage: `url(${images})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
        className="h-screen relative bg-[#071235] text-white flex flex-col items-center justify-center px-6 md:px-12 lg:px-20 text-center"
      >
        <div className="absolute inset-0">
          <img src={globe} alt="" className="h-full w-full object-cover opacity-40" />
        </div>
        <div className="z-10">
          <h1 className="text-4xl md:text-6xl font-black leading-tight mb-6">
            Welcome To <span className="text-[#5380ea]">Apk </span>Trust
          </h1>
          <p className="max-w-2xl mx-auto text-sm md:text-base leading-relaxed mb-10">
            Scan Your Apk With Machine Learning Technology. Protect Your
            Smartphone From Malware, Trojans, And Hidden Threats — before It’s
            Too Late.
          </p>

          <button
            onClick={() => navigate("/upload")}
            className="bg-[#2478fe] hover:bg-[#3c8fff] transition-colors rounded-lg px-6 py-3 font-semibold text-white"
          >
            Upload Apk Now
          </button>
        </div>
      </section>

      {/* ABOUT SECTION */}
      <section
        id="about"
        className="min-h-screen bg-[#071235] text-white flex flex-col items-center justify-center px-6 md:px-12 lg:px-20"
      >
        <div className="flex flex-col lg:flex-row justify-between items-center w-full">
          <div className="w-full lg:w-1/2">
            <h2 className="text-4xl md:text-5xl font-black mb-6">
              About <span className="text-[#ffa700]">Apk Trust</span>
            </h2>
            <p className="max-w-3xl text-base text-left md:text-lg mb-12">
              Apk Trust adalah platform analisis keamanan aplikasi Android
              berbasis Machine Learning. Kami membantu pengguna memeriksa apakah
              sebuah APK mengandung kode berbahaya atau tidak sebelum diinstal.
            </p>

            <h3 className="text-[#ffd328] text-2xl font-bold mb-10 text-center md:text-left">
              How It Works?
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl w-full">
              <div className="flex flex-col items-center space-y-3">
                <img
                  src={uploadapk}
                  className="w-40 sm:w-48 md:w-56 lg:w-64 h-auto transition-transform duration-300 hover:scale-105"
                />
              </div>

              <div className="flex flex-col items-center space-y-3">
                <img
                  src={autos}
                  className="w-40 sm:w-48 md:w-56 lg:w-64 h-auto transition-transform duration-300 hover:scale-105"
                />
              </div>

              <div className="flex flex-col items-center space-y-3">
                <img
                  src={result}
                  className="w-40 sm:w-48 md:w-56 lg:w-64 h-auto transition-transform duration-300 hover:scale-105"
                />
              </div>
            </div>
          </div>

          {/* 🔄 Gambar keyabout berputar & responsif */}
          <div className="w-full lg:w-1/2 flex justify-center mt-10 lg:mt-0">
            <motion.img
              src={keyabout}
              alt="About Illustration"
              className="w-60 sm:w-72 md:w-80 lg:w-96 max-w-full object-contain"
              animate={{ rotate: 360 }}
              transition={{
                repeat: Infinity,
                duration: 12,
                ease: "linear",
              }}
            />
          </div>
        </div>
      </section>

      {/* FAQ SECTION */}
      <section
        id="faq"
        className="min-h-screen flex flex-col items-center justify-center bg-[#0b1439] text-white px-6"
      >
        <h2 className="text-4xl md:text-5xl font-black mb-16">
          <span className="text-[#5380ea]">FAQ </span>Section
        </h2>
        <p className="max-w-2xl text-center text-base md:text-lg opacity-80">
          Pertanyaan yang sering diajukan tentang cara kerja, keamanan, dan
          penggunaan APK Trust.
        </p>
      </section>

      {/* CONTACT SECTION */}
      <section
        id="contact"
        className="min-h-screen flex flex-col bg-[#00091f] text-center text-white items-center justify-between"
      >
        <div className="m-20">
          <h2 className="text-4xl md:text-5xl font-black mb-16">
            <span className="text-[#5380ea]">Contact </span>Us
          </h2>
          <p className="max-w-2xl mx-auto text-base md:text-lg opacity-80">
            Hubungi kami untuk pertanyaan lebih lanjut, kolaborasi, atau dukungan teknis.
          </p>
        </div>
        <div className="w-full bg-[#071235] py-8 rounded-t-3xl">
          <p className="text-sm text-gray-300">© 2025 APK Trust. All Rights Reserved.</p>
        </div>
      </section>
    </div>
  );
};

export default Home;
