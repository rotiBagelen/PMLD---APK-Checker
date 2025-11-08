import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import worlda from "../assets/bg/world.png";

const DetailApkPage: React.FC = () => {
  const navigate = useNavigate();
  const [year, setYear] = useState<number>(new Date().getFullYear());

  useEffect(() => {
    setYear(new Date().getFullYear());
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#071235] via-[#0b1444] to-[#20164b] text-white relative overflow-hidden">
      {/* 🔵 Efek Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-80 sm:w-96 h-80 sm:h-96 bg-blue-500/20 rounded-full blur-[120px] top-20 left-10"></div>
        <div className="absolute w-60 sm:w-72 h-60 sm:h-72 bg-purple-500/20 rounded-full blur-[120px] bottom-10 right-20"></div>
        <div className="absolute w-48 sm:w-60 h-48 sm:h-60 bg-indigo-400/20 rounded-full blur-[120px] top-1/3 right-1/3"></div>
      </div>

      {/* 🔹 Navbar */}
      <nav className="fixed top-0 left-0 w-full bg-[#0b1137]/60 backdrop-blur-xl border-b border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.1)] z-50 transition-all duration-300">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 md:px-12 py-4">
          {/* Logo */}
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

          {/* Menu */}
          <div className="flex items-center space-x-8">
            <button
              onClick={() => navigate("/")}
              className="text-white/90 hover:text-[#8AB6FF] transition-colors font-semibold"
            >
              Home
            </button>

            <button
              onClick={() => navigate("/upload")}
              className="relative overflow-hidden group text-white font-semibold px-6 py-2 rounded-full bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] hover:from-[#88b4ff] hover:to-[#5d93ff] shadow-md hover:shadow-[#7BA5FF]/30 transition-all duration-300"
            >
              <span className="relative z-10">Upload APK</span>
              <div className="absolute inset-0 bg-gradient-to-r from-[#7BA5FF] to-[#3B82F6] opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-full"></div>
            </button>
          </div>
        </div>
      </nav>

      {/* 🔹 Konten Halaman */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-20 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Kiri - Detail */}
          <section className="lg:col-span-2 space-y-6">
            <article className="bg-[#0c184b]/60 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 p-5 sm:p-6">
              <div className="flex flex-col sm:flex-row items-start gap-6">
                <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-lg bg-gradient-to-br from-[#2c4ef8]/20 to-[#5380ea]/30 flex items-center justify-center shrink-0">
                  <img
                    src="https://c.animaapp.com/mgji03kiAEZ1ph/img/upload-apk.png"
                    alt="upload"
                    className="object-contain w-16 h-16 sm:w-20 sm:h-20"
                  />
                </div>

                <div className="flex-1">
                  <h1 className="text-xl sm:text-2xl font-semibold">
                    Detail Information <span className="text-slate-400">— Model Xxx</span>
                  </h1>
                  <p className="mt-2 text-sm text-slate-400">
                    Ringkasan skor aplikasi, informasi file, dan detail perizinan ditampilkan di halaman ini.
                  </p>

                  {/* Info */}
                  <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="p-4 rounded-lg border border-white/20 bg-white/5">
                      <h3 className="text-sm font-medium text-[#8fb3ff]">App Scores</h3>
                      <div className="mt-2 space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Security Score:</span>
                          <span className="font-semibold">Xx</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Trackers Detection:</span>
                          <span className="font-semibold">Xx</span>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 rounded-lg border border-white/20 bg-white/5">
                      <h3 className="text-sm font-medium text-[#8fb3ff]">File Information</h3>
                      <div className="mt-2 space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>File Name:</span>
                          <span className="font-mono">Xx.apk</span>
                        </div>
                        <div className="flex justify-between">
                          <span>MD5:</span>
                          <span className="font-mono">Xx</span>
                        </div>
                        <div className="flex justify-between">
                          <span>SHA1:</span>
                          <span className="font-mono">Xx</span>
                        </div>
                        <div className="flex justify-between">
                          <span>SHA256:</span>
                          <span className="font-mono">Xx</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Size:</span>
                          <span className="font-mono">Xx MB</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* App Info */}
                  <div className="mt-6 p-4 rounded-lg border border-white/20 bg-white/5">
                    <h3 className="text-sm font-medium text-[#8fb3ff]">App Information</h3>
                    <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                      <div className="flex justify-between">
                        <span>Package:</span>
                        <span className="font-mono">com.example.xxx</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Version:</span>
                        <span className="font-mono">Xx</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Min SDK:</span>
                        <span className="font-mono">Xx</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Target SDK:</span>
                        <span className="font-mono">Xx</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </article>

            {/* 🔹 Analysis Section (baru) */}
            <article className="bg-[#0c184b]/60 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 p-5">
              <h2 className="text-lg font-semibold mb-3 text-[#8fb3ff]">Analisis</h2>
              <p className="text-sm text-slate-300 leading-relaxed">
                Hasil analisis menunjukkan bahwa aplikasi ini <span className="text-green-400 font-semibold">aman</span> untuk digunakan.
                Tidak ditemukan indikasi aktivitas berbahaya, namun terdapat beberapa izin akses yang perlu diperhatikan
                seperti <span className="font-mono text-slate-400">READ_CONTACTS</span> dan <span className="font-mono text-slate-400">INTERNET</span>.
                Berdasarkan skor keamanan dan deteksi pelacak, aplikasi ini dinilai memiliki tingkat risiko rendah.
              </p>
            </article>

            {/* 🔹 Analysis Section (baru) */}
            <article className="bg-[#0c184b]/60 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 p-5">
              <h2 className="text-lg font-semibold mb-3 text-[#8fb3ff]">Analisis API Sensitif</h2>
              <p className="text-sm text-slate-300 leading-relaxed">
                Hasil analisis menunjukkan bahwa aplikasi ini <span className="text-green-400 font-semibold">aman</span> untuk digunakan.
                Tidak ditemukan indikasi aktivitas berbahaya, namun terdapat beberapa izin akses yang perlu diperhatikan
                seperti <span className="font-mono text-slate-400">READ_CONTACTS</span> dan <span className="font-mono text-slate-400">INTERNET</span>.
                Berdasarkan skor keamanan dan deteksi pelacak, aplikasi ini dinilai memiliki tingkat risiko rendah.
              </p>
            </article>

            {/* Permissions Table */}
            <article className="bg-[#0c184b]/60 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 p-4 overflow-x-auto">
              <h2 className="text-lg font-semibold mb-3 text-[#8fb3ff]">Permissions</h2>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[680px] text-sm border-collapse">
                  <thead className="bg-white/10 text-left">
                    <tr>
                      <th className="px-4 py-2">PERMISSIONS</th>
                      <th className="px-4 py-2">STATUS</th>
                      <th className="px-4 py-2">INFO</th>
                      <th className="px-4 py-2">DESCRIPTION</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-t border-white/10">
                      <td className="px-4 py-3">android.permission.INTERNET</td>
                      <td className="px-4 py-3 text-green-400">Allowed</td>
                      <td className="px-4 py-3">Network access</td>
                      <td className="px-4 py-3">Uses network</td>
                    </tr>
                    <tr className="border-t border-white/10">
                      <td className="px-4 py-3">android.permission.READ_CONTACTS</td>
                      <td className="px-4 py-3 text-red-400">Denied</td>
                      <td className="px-4 py-3">Access contacts</td>
                      <td className="px-4 py-3">--</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </article>
          </section>

          {/* Kanan - Sidebar */}
          <aside className="space-y-6">
            <div className="bg-[#0c184b]/60 rounded-2xl border border-white/10 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-[#8fb3ff]">Quick Summary</h3>
                  <p className="text-xs text-slate-400 mt-1">Ringkasan utama aplikasi</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">-</div>
                  <div className="text-xs text-slate-400">App Scores</div>
                </div>
              </div>

              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Signed:</span>
                  <span className="font-semibold">Yes</span>
                </div>
                <div className="flex justify-between">
                  <span>Potential trackers:</span>
                  <span className="font-semibold">X</span>
                </div>
                <div className="flex justify-between">
                  <span>Malicious:</span>
                  <span className="font-semibold text-green-400">No</span>
                </div>
              </div>
            </div>

            <div className="bg-[#0c184b]/60 rounded-2xl border border-white/10 p-5">
              <h4 className="text-sm font-medium text-[#8fb3ff]">Details</h4>
              <ul className="mt-3 text-sm space-y-2">
                <li className="flex justify-between">
                  <span>Uploaded</span>
                  <span className="font-mono">Xx</span>
                </li>
                <li className="flex justify-between">
                  <span>Scanned</span>
                  <span className="font-mono">Xx</span>
                </li>
                <li className="flex justify-between">
                  <span>Last update</span>
                  <span className="font-mono">Xx</span>
                </li>
              </ul>
            </div>

            <div className="bg-[#0c184b]/60 rounded-2xl border border-white/10 p-5 text-center">
              <img
                src="https://c.animaapp.com/mgji03kiAEZ1ph/img/arcticons-trustdock.svg"
                alt="trust"
                className="mx-auto h-12 w-12"
              />
              <p className="mt-3 text-sm text-slate-400">Brand / Trust badge</p>
              <Link
                to="/upload"
                className="mt-4 inline-block w-full px-3 py-2 bg-[#5380ea] hover:bg-[#3c6ff7] text-white rounded-md"
              >
                Analyze Another APK
              </Link>
            </div>
          </aside>
        </div>
      </main>

      {/* 🔹 Footer */}
      <footer className="border-t border-white/10 text-center py-5 text-xs sm:text-sm text-white/70 px-4">
        © {year} APK TRUST — All Rights Reserved.
      </footer>
    </div>
  );
};

export default DetailApkPage;
