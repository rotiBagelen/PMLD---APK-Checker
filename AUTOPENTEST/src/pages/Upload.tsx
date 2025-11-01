import { useState } from "react";
import { ArrowDownToLine, Menu, X } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import images from "../assets/bg/bg.png";
import worlda from "../assets/bg/world.png";

// 🌟 Navbar Premium Elegan (Home + Upload)
const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const isActive = (path: string) =>
    location.pathname === path
      ? "text-[#8AB6FF] font-semibold border-b-2 border-[#8AB6FF] pb-1"
      : "text-white/90 hover:text-[#8AB6FF] transition-colors";

  return (
    <nav className="fixed top-0 left-0 w-full bg-[#0b1137]/60 backdrop-blur-xl border-b border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.1)] z-50 transition-all duration-300">
      <div className="w-full flex items-center justify-between px-6 md:px-12 py-4">
        {/* Logo kiri */}
        <div
          onClick={() => navigate("/")}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="relative">
            <img
              src={worlda}
              alt="APK Trust Logo"
              className="w-10 h-10 transition-transform duration-300 group-hover:rotate-12"
            />
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] opacity-0 group-hover:opacity-30 blur-md transition-all duration-500"></div>
          </div>
          <span className="font-bold text-lg md:text-xl tracking-wide text-white group-hover:text-[#8AB6FF] transition-all">
            APK TRUST
          </span>
        </div>

        {/* Menu kanan */}
        <div className="hidden md:flex items-center space-x-8">
          <button onClick={() => navigate("/")} className={isActive("/")}>
            Home
          </button>

          <button
            onClick={() => navigate("/upload")}
            className={`relative overflow-hidden group text-white font-semibold px-6 py-2 rounded-full transition-all duration-300 ${
              location.pathname === "/upload"
                ? "bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6]"
                : "bg-[#3B82F6]/90 hover:bg-[#5380ea]"
            } shadow-md hover:shadow-[#7BA5FF]/30`}
          >
            <span className="relative z-10">Upload APK</span>
            <div className="absolute inset-0 bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-full"></div>
          </button>
        </div>

        {/* Tombol menu mobile */}
        <button
          className="md:hidden text-white"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Dropdown Mobile */}
      {menuOpen && (
        <div className="md:hidden absolute top-[72px] right-4 bg-[#0B1137]/95 backdrop-blur-lg rounded-2xl shadow-lg p-5 flex flex-col space-y-4 border border-white/10 w-48 animate-fadeIn">
          <button
            onClick={() => {
              navigate("/");
              setMenuOpen(false);
            }}
            className={`${isActive("/")} text-left`}
          >
            Home
          </button>
          <button
            onClick={() => {
              navigate("/upload");
              setMenuOpen(false);
            }}
            className={`w-full text-center px-4 py-2 rounded-lg font-semibold ${
              location.pathname === "/upload"
                ? "bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6]"
                : "bg-[#3B82F6] hover:bg-[#5380ea]"
            } text-white shadow-md`}
          >
            Upload APK
          </button>
        </div>
      )}
    </nav>
  );
};

// ✅ Halaman Upload
export default function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      alert("Please select an APK file first!");
      return;
    }
    navigate("/result");
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-[#0A0F2D] to-[#0B1137] text-white relative px-6"
      style={{
        backgroundImage: `url(${images})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* ✅ Navbar */}
      <Navbar />

      {/* ✅ Konten Upload */}
      <div className="flex flex-col md:flex-row items-center justify-center gap-10 md:gap-20 mt-32 w-full max-w-6xl">
        {/* Kiri - Deskripsi */}
        <div className="text-center md:text-left max-w-md">
          <h1 className="text-5xl md:text-6xl font-bold text-[#7BA5FF] drop-shadow-md">
            APK<span className="text-white">Trust</span>
          </h1>
          <div className="text-[#7BA5FF] font-semibold text-lg mt-3">—</div>
          <p className="text-gray-300 mt-4 leading-relaxed">
            A modern mobile application for digital trust & security verification.
          </p>
        </div>

        {/* Kanan - Form Upload */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col items-center bg-white/10 backdrop-blur-md rounded-2xl p-8 w-full sm:w-96 shadow-lg border border-white/20 transition-all hover:shadow-[#7BA5FF]/30"
        >
          <ArrowDownToLine className="w-20 h-20 text-[#3B82F6] animate-bounce" />
          <p className="text-gray-300 mt-4 mb-4 text-center">
            UPLOAD YOUR APP HERE!
          </p>

          <input
            type="file"
            accept=".apk"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="mb-4 w-full text-sm text-gray-200 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-[#3B82F6] file:text-white hover:file:bg-blue-600 cursor-pointer"
          />

          <button
            type="submit"
            className="mt-2 bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] hover:from-[#88b4ff] hover:to-[#5d93ff] text-white px-6 py-2 rounded-xl transition-all w-full font-semibold shadow-md hover:shadow-[#3B82F6]/40"
          >
            Check APK Now
          </button>
        </form>
      </div>
    </div>
  );
}
