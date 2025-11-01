import { useState,useEffect } from "react";
import { Gauge, ShieldAlert, Menu, X } from "lucide-react";
import { useNavigate } from "react-router-dom";
import worlda from "../assets/bg/world.png";
import { Loader2 } from "lucide-react";

const Report = () => {
  const [loading, setLoading] = useState(true);
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const navigate = useNavigate();

  const API_URL = "http://localhost:5000/api/report/latest";

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("Gagal mengambil data laporan");
        const data = await res.json();
        setReportData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-600">
        <Loader2 className="animate-spin w-6 h-6 mr-2" />
        Memuat laporan analisis...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen text-red-600">
        ❌ {error}
      </div>
    );
  }

  if (!reportData) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-500">
        Tidak ada data laporan ditemukan.
      </div>
    );
  }

  // === Ambil Data ===
  const { ml_results = [], mobsf_report = {} } = reportData;

  // ✅ Hitung status keamanan dari hasil ML
  const safeCount = ml_results.filter(
    (r) => r.Hasil_Prediksi === "Terlihat Aman"
  ).length;
  const status = safeCount >= 2 ? "Safe" : "Dangerous";

  // ✅ Ambil security score dari MobSF
  const securityScore =
    mobsf_report?.security_score ||
    mobsf_report?.score ||
    mobsf_report?.analysis_info?.security_score ||
    "N/A";

  // ✅ Hitung rata-rata kepercayaan model
  const avgConfidence =
    ml_results.length > 0
      ? (
          ml_results.reduce(
            (sum, r) => sum + (r.Kepercayaan_Berbahaya || 0),
            0
          ) / ml_results.length
        ).toFixed(2)
      : "0";

const ResultPage = () => {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [showDetail, setShowDetail] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#071235] via-[#0b1444] to-[#20164b] text-white relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-80 sm:w-96 h-80 sm:h-96 bg-blue-500/20 rounded-full blur-[120px] top-20 left-10"></div>
        <div className="absolute w-60 sm:w-72 h-60 sm:h-72 bg-purple-500/20 rounded-full blur-[120px] bottom-10 right-20"></div>
        <div className="absolute w-48 sm:w-60 h-48 sm:h-60 bg-indigo-400/20 rounded-full blur-[120px] top-1/3 right-1/3"></div>
      </div>

      {/* ✅ Navbar */}
      <nav className="fixed top-0 left-0 w-full bg-[#0b1137]/60 backdrop-blur-xl border-b border-white/10 z-50">
        <div className="flex items-center justify-between px-6 md:px-12 py-4">
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

          <div className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => navigate("/")}
              className="text-white/90 hover:text-[#8AB6FF] transition-colors"
            >
              Home
            </button>

            <button
              onClick={() => navigate("/upload")}
              className="relative overflow-hidden group text-white font-semibold px-6 py-2 rounded-full transition-all duration-300 bg-[#3B82F6]/90 hover:bg-[#5380ea] shadow-md hover:shadow-[#7BA5FF]/30"
            >
              <span className="relative z-10">Upload APK</span>
              <div className="absolute inset-0 bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-full"></div>
            </button>
          </div>

          <button
            className="md:hidden text-white"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>

        {menuOpen && (
          <div className="md:hidden absolute top-[72px] right-4 bg-[#0B1137]/95 backdrop-blur-lg rounded-2xl shadow-lg p-5 flex flex-col space-y-4 border border-white/10 w-48">
            <button
              onClick={() => {
                navigate("/");
                setMenuOpen(false);
              }}
              className="text-white/90 hover:text-[#8AB6FF] text-left"
            >
              Home
            </button>
            <button
              onClick={() => {
                navigate("/upload");
                setMenuOpen(false);
              }}
              className="w-full text-center px-4 py-2 rounded-lg font-semibold bg-[#3B82F6] hover:bg-[#5380ea] text-white shadow-md"
            >
              Upload APK
            </button>
          </div>
        )}
      </nav>

      {/* 🌟 Main Content */}
      <main className="pt-32 sm:pt-40 pb-16 flex flex-col items-center z-10 relative px-4 sm:px-6">
        <h1 className="text-3xl sm:text-5xl font-extrabold text-center mb-2 tracking-wide">
          RESULT
        </h1>
        <div className="w-16 sm:w-20 h-[3px] bg-[#5380ea] rounded-full mb-10 sm:mb-12"></div>

        <div className="flex flex-col items-center lg:flex-row gap-10 lg:gap-16 w-full max-w-7xl justify-center">
          <div className="flex flex-col items-center gap-6">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              {/* STATUS */}
              <div className="relative bg-gradient-to-b from-[#0c1a3d] to-[#1a2760] rounded-2xl shadow-[0_0_30px_rgba(83,128,234,0.15)] w-64 sm:w-72 h-60 sm:h-64 flex flex-col items-center justify-center border border-white/10">
                <div className="absolute -top-5 bg-gradient-to-r from-[#ffb100] to-[#ffcc4d] text-[#071235] font-bold px-5 py-1 rounded-md shadow-md">
                  STATUS
                </div>
                <ShieldAlert
                  size={64}
                  className="text-[#4285F4] mb-4 drop-shadow-[0_0_8px_rgba(66,133,244,0.6)]"
                />
                <p className="text-[#9db2ff]/80 font-medium text-sm">
                  Status Apk :
                </p>
              </div>

              {/* Average Model */}
              <div className="relative bg-gradient-to-b from-[#0c1a3d] to-[#1a2760] rounded-2xl shadow-[0_0_30px_rgba(83,128,234,0.15)] w-64 sm:w-72 h-60 sm:h-64 flex flex-col items-center justify-center border border-white/10">
                <div className="absolute -top-5 bg-gradient-to-r from-[#ffb100] to-[#ffcc4d] text-[#071235] font-bold px-5 py-1 rounded-md shadow-md">
                  Average Model
                </div>
                <Gauge
                  size={64}
                  className="text-[#4285F4] mb-4 drop-shadow-[0_0_8px_rgba(66,133,244,0.6)]"
                />
                <p className="text-[#9db2ff]/80 font-medium text-sm">
                  Security Score :
                </p>
              </div>
            </div>

            {/* Tombol Detail */}
            <button
              onClick={() => setShowDetail(!showDetail)}
              className="bg-gradient-to-r from-[#ffb100] to-[#ffcc4d] text-[#071235] font-bold px-8 sm:px-10 py-2 rounded-md shadow-[0_0_15px_rgba(255,177,0,0.4)] hover:shadow-[0_0_25px_rgba(255,204,77,0.7)] hover:scale-[1.05] transition duration-300 mt-4 text-sm sm:text-base"
            >
              {showDetail ? "Sembunyikan Detail" : "Detail"}
            </button>
          </div>

          {/* MODEL PERFORMANCE */}
          <div className="bg-[#0e1a4a]/50 rounded-2xl border border-[#5380ea]/50 px-6 py-10 shadow-[0_0_25px_rgba(83,128,234,0.15)] w-full lg:w-auto">
            <div className="bg-[#5380ea] px-6 py-1 rounded-md text-center font-semibold text-white w-max mx-auto mb-10 text-sm sm:text-base">
              MODEL PERFORMANCE
            </div>

            <div className="flex flex-wrap gap-6 justify-center items-center">
              {/* RandomForest */}
              <div className="bg-gradient-to-br from-[#3a2158] to-[#5c3b85] rounded-2xl w-52 h-52 flex flex-col items-center justify-center hover:scale-[1.05] transition duration-300">
                <Gauge size={56} className="text-white mb-4" />
                <p className="font-semibold text-sm">RandomForest</p>
              </div>

              {/* SVM RBF */}
              <div className="bg-gradient-to-br from-[#14244d] to-[#243b6a] rounded-2xl w-52 h-52 flex flex-col items-center justify-center hover:scale-[1.05] transition duration-300">
                <Gauge size={56} className="text-white mb-4" />
                <p className="font-semibold text-sm">SVM RBF</p>
              </div>

              {/* XGBoost */}
              <div className="bg-gradient-to-br from-[#3c2c1d] to-[#6b4c2c] rounded-2xl w-52 h-52 flex flex-col items-center justify-center hover:scale-[1.05] transition duration-300">
                <Gauge size={56} className="text-white mb-4" />
                <p className="font-semibold text-sm">XGBoost</p>
              </div>

              {/* 🌟 GradientBoosting (baru ditambahkan) */}
              <div className="bg-gradient-to-br from-[#1d3c2c] to-[#2c6b4c] rounded-2xl w-52 h-52 flex flex-col items-center justify-center hover:scale-[1.05] transition duration-300">
                <Gauge size={56} className="text-white mb-4" />
                <p className="font-semibold text-sm">GradientBoosting</p>
              </div>
            </div>
          </div>
        </div>

        {/* Detail Section */}
        {showDetail && (
          <div className="mt-16 w-full max-w-6xl space-y-8 animate-fadeIn">
            <div className="bg-[#0e1a4a]/60 border border-white/10 rounded-2xl p-6 shadow-[0_0_20px_rgba(83,128,234,0.15)]">
              <h2 className="text-xl font-semibold text-[#8AB6FF] mb-3">
                Analisis
              </h2>
              <p className="text-white/80 leading-relaxed text-sm">
                Hasil analisis menunjukkan bahwa aplikasi ini{" "}
                <span className="text-green-400 font-semibold">aman</span> untuk digunakan.
                Tidak ditemukan indikasi aktivitas berbahaya, namun terdapat beberapa izin
                akses seperti <span className="text-[#7BA5FF]">READ_CONTACTS</span> dan{" "}
                <span className="text-[#7BA5FF]">INTERNET</span>.
              </p>
            </div>

            <div className="bg-[#0e1a4a]/60 border border-white/10 rounded-2xl p-6 shadow-[0_0_20px_rgba(83,128,234,0.15)]">
              <h2 className="text-xl font-semibold text-[#8AB6FF] mb-3">
                Analisis API Sensitif
              </h2>
              <p className="text-white/80 leading-relaxed text-sm">
                Berdasarkan skor keamanan dan deteksi pelacak, aplikasi ini dinilai{" "}
                <span className="text-green-400 font-semibold">memiliki risiko rendah</span>.
                Tidak ditemukan indikasi aktivitas mencurigakan pada API sensitif.
              </p>
            </div>

            <div className="bg-[#0e1a4a]/60 border border-white/10 rounded-2xl p-6 shadow-[0_0_20px_rgba(83,128,234,0.15)]">
              <h2 className="text-xl font-semibold text-[#8AB6FF] mb-4">Permissions</h2>
              <div className="overflow-x-auto">
                <table className="w-full border border-white/10 text-sm">
                  <thead className="bg-[#142a58]/60">
                    <tr>
                      <th className="px-4 py-2 text-left border-b border-white/10">
                        PERMISSIONS
                      </th>
                      <th className="px-4 py-2 text-left border-b border-white/10">STATUS</th>
                      <th className="px-4 py-2 text-left border-b border-white/10">INFO</th>
                      <th className="px-4 py-2 text-left border-b border-white/10">
                        DESCRIPTION
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="hover:bg-white/5 transition">
                      <td className="px-4 py-2 border-b border-white/10">
                        android.permission.INTERNET
                      </td>
                      <td className="px-4 py-2 border-b border-white/10 text-green-400 font-medium">
                        Allowed
                      </td>
                      <td className="px-4 py-2 border-b border-white/10">Network access</td>
                      <td className="px-4 py-2 border-b border-white/10">Uses network</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition">
                      <td className="px-4 py-2 border-b border-white/10">
                        android.permission.READ_CONTACTS
                      </td>
                      <td className="px-4 py-2 border-b border-white/10 text-red-400 font-medium">
                        Denied
                      </td>
                      <td className="px-4 py-2 border-b border-white/10">Access contacts</td>
                      <td className="px-4 py-2 border-b border-white/10">--</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-white/10 text-center py-5 text-xs sm:text-sm text-white/70">
        © 2025 APK TRUST — All Rights Reserved.
      </footer>
    </div>
  );
};

export default ResultPage;
