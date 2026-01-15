/* ==========================================
   MODERN CV/RESUME WEBSITE JAVASCRIPT
   All interactive features and animations
   ========================================== */

// ============================================
// 0. ADAPTIVE COLOR THEME FROM PROFILE IMAGE
// ============================================
function extractColorsFromImage() {
  // Use the hero profile image (profile1.jpg)
  const img = document.querySelector(".hero-image img");
  if (!img) return;

  const canvas = document.getElementById("colorCanvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  // Wait for image to load
  if (!img.complete) {
    img.addEventListener("load", () => extractColorsFromImage());
    return;
  }

  try {
    // Set canvas size using natural dimensions
    canvas.width = img.naturalWidth || img.width;
    canvas.height = img.naturalHeight || img.height;

    // Draw image
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    // Get image data
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;

    // Extract dominant colors with better algorithm
    const colorMap = {};
    const saturationMap = {};

    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];
      const a = pixels[i + 3];

      // Skip transparent or extreme pixels
      if (
        a < 125 ||
        (r < 20 && g < 20 && b < 20) ||
        (r > 235 && g > 235 && b > 235)
      ) {
        continue;
      }

      // Calculate saturation and brightness
      const max = Math.max(r, g, b) / 255;
      const min = Math.min(r, g, b) / 255;
      const l = (max + min) / 2;
      const s =
        max === min
          ? 0
          : l > 0.5
          ? (max - min) / (2 - max - min)
          : (max - min) / (max + min);

      // Only include colors with decent saturation
      if (s > 0.2) {
        const key = `${Math.floor(r / 15) * 15},${Math.floor(g / 15) * 15},${
          Math.floor(b / 15) * 15
        }`;
        colorMap[key] = (colorMap[key] || 0) + 1;
        saturationMap[key] = s;
      }
    }

    // Sort by frequency and saturation
    const sortedColors = Object.entries(colorMap)
      .map(([color, count]) => ({
        color,
        count,
        saturation: saturationMap[color],
      }))
      .sort((a, b) => {
        // Prioritize both frequency and saturation
        return b.count * b.saturation - a.count * a.saturation;
      })
      .slice(0, 15);

    if (sortedColors.length === 0) return;

    // Find the best accent color (most vibrant)
    let accentColor = null;
    let secondaryColor = null;

    for (const item of sortedColors) {
      const [r, g, b] = item.color.split(",").map(Number);

      // Calculate HSL
      const max = Math.max(r, g, b) / 255;
      const min = Math.min(r, g, b) / 255;
      const l = (max + min) / 2;
      const s =
        max === min
          ? 0
          : l > 0.5
          ? (max - min) / (2 - max - min)
          : (max - min) / (max + min);

      // Get hue
      let h = 0;
      if (max !== min) {
        switch (max) {
          case r / 255:
            h = ((g - b) / 255 / (max - min) + (g < b ? 6 : 0)) / 6;
            break;
          case g / 255:
            h = ((b - r) / 255 / (max - min) + 2) / 6;
            break;
          case b / 255:
            h = ((r - g) / 255 / (max - min) + 4) / 6;
            break;
        }
      }

      // Look for vibrant colors with better brightness (avoid dark colors)
      if (!accentColor && s > 0.35 && l > 0.35 && l < 0.85) {
        // Boost the color for better visibility and brightness
        const boosted = boostSaturation(r, g, b, 1.4);
        const brightened = boostBrightness(
          boosted.r,
          boosted.g,
          boosted.b,
          1.2
        );
        accentColor = `rgb(${brightened.r}, ${brightened.g}, ${brightened.b})`;
      }

      // Find a different color for secondary
      if (accentColor && !secondaryColor && s > 0.25) {
        const [r1, g1, b1] = sortedColors[0].color.split(",").map(Number);
        const colorDiff =
          Math.abs(r - r1) + Math.abs(g - g1) + Math.abs(b - b1);

        if (colorDiff > 50) {
          secondaryColor = `rgb(${Math.floor(r * 0.8)}, ${Math.floor(
            g * 0.8
          )}, ${Math.floor(b * 0.8)})`;
        }
      }

      if (accentColor && secondaryColor) break;
    }

    // Fallback: use most prominent color with strong boost and brightness increase
    if (!accentColor) {
      const [r, g, b] = sortedColors[0].color.split(",").map(Number);
      const boosted = boostSaturation(r, g, b, 1.8);
      // Make it brighter by scaling up RGB values
      const brightR = Math.min(255, Math.round(boosted.r * 1.3));
      const brightG = Math.min(255, Math.round(boosted.g * 1.3));
      const brightB = Math.min(255, Math.round(boosted.b * 1.3));
      accentColor = `rgb(${brightR}, ${brightG}, ${brightB})`;
    }

    if (!secondaryColor) {
      const [r, g, b] = sortedColors[0].color.split(",").map(Number);
      secondaryColor = `rgb(${Math.floor(r * 0.6)}, ${Math.floor(
        g * 0.6
      )}, ${Math.floor(b * 0.6)})`;
    }

    // Apply colors to CSS variables
    const root = document.documentElement;
    root.style.setProperty("--primary-color", accentColor);
    root.style.setProperty("--secondary-color", secondaryColor);
    root.style.setProperty("--accent-neon", accentColor);
    root.style.setProperty("--accent-green", accentColor);

    // Store in localStorage for persistence
    localStorage.setItem(
      "adaptiveColors",
      JSON.stringify({
        primary: accentColor,
        secondary: secondaryColor,
      })
    );

    console.log("🎨 Adaptive colors applied from profile image:", {
      primary: accentColor,
      secondary: secondaryColor,
      extracted: sortedColors.length + " colors analyzed",
    });
  } catch (error) {
    console.log(
      "⚠️ Color extraction skipped (CORS or loading issue). Using default colors."
    );
  }
}

// Helper function to boost color saturation
function boostSaturation(r, g, b, factor) {
  // Convert to HSL
  r /= 255;
  g /= 255;
  b /= 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h,
    s,
    l = (max + min) / 2;

  if (max === min) {
    h = s = 0;
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }
  }

  // Boost saturation
  s = Math.min(1, s * factor);

  // Convert back to RGB
  let r2, g2, b2;
  if (s === 0) {
    r2 = g2 = b2 = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r2 = hue2rgb(p, q, h + 1 / 3);
    g2 = hue2rgb(p, q, h);
    b2 = hue2rgb(p, q, h - 1 / 3);
  }

  return {
    r: Math.round(r2 * 255),
    g: Math.round(g2 * 255),
    b: Math.round(b2 * 255),
  };
}

// Helper function to boost color brightness
function boostBrightness(r, g, b, factor = 1.2) {
  // Increase brightness while maintaining color ratio
  r = Math.min(255, r * factor);
  g = Math.min(255, g * factor);
  b = Math.min(255, b * factor);

  return {
    r: Math.round(r),
    g: Math.round(g),
    b: Math.round(b),
  };
}

// Load saved colors on page load
function loadSavedColors() {
  const saved = localStorage.getItem("adaptiveColors");
  if (saved) {
    const colors = JSON.parse(saved);
    const root = document.documentElement;
    root.style.setProperty("--primary-color", colors.primary);
    root.style.setProperty("--secondary-color", colors.secondary);
    root.style.setProperty("--accent-neon", colors.primary);
    root.style.setProperty("--accent-green", colors.primary);
    console.log("🎨 Loaded saved colors:", colors);
  }
}

// Load saved colors immediately to prevent yellow flash
loadSavedColors();

// Initialize adaptive colors on page load
window.addEventListener("DOMContentLoaded", function () {
  // Extract colors quickly
  setTimeout(() => extractColorsFromImage(), 300);
});

// Also try on window load for better reliability
window.addEventListener("load", function () {
  setTimeout(() => extractColorsFromImage(), 100);
});

// ============================================
// 1. LANGUAGE TRANSLATION SYSTEM
// ============================================
const translations = {
  id: {
    niceToMeet: "Senang Bertemu Anda",
    aboutMe: "Tentang Saya",
    age: "Usia:",
    residence: "Tempat Tinggal:",
    freelance: "Freelance:",
    available: "Tersedia",
    address: "Alamat:",
    heroTitle:
      "Mechatronics Engineer | Data & Digitalization Specialist | Marketing Analytics",
    heroDesc1:
      "Mechatronics Engineer dengan pengalaman kerja formal 5+ tahun di bidang automotive engineering, product testing, data analysis, marketing, dan digitalisasi bisnis. Saya menghubungkan engineering execution, data-driven insight, dan digital systems untuk membantu organisasi meningkatkan efisiensi operasional, visibilitas, dan performa pasar.",
    heroDesc2:
      "Dengan pengalaman di manufacturing operations, prototyping, dan cross-functional digitalization, saya terbiasa melihat masalah dari dua sisi: technical reality dan business impact. Saya mengembangkan web-based solutions menggunakan Laravel dan menganalisis market trends melalui SEO dan marketing analytics.",
    mySkills: "Keahlian Saya",
    skillsPortfolio: "Keahlian & Portofolio",

    // Domain 1: Engineering & Manufacturing
    domain1_title: "Rekayasa & Manufaktur",
    skill1_1_title:
      "Arsitektur Sistem Elektrikal & Troubleshooting Lapangan (3W ICE)",
    skill1_1_desc:
      "Memimpin pemecahan dan dokumentasi sistem kelistrikan lengkap kendaraan ICE roda 3 menjadi diagram yang jelas dan mudah dipahami untuk pemecahan masalah lapangan. Sistem ini mendukung troubleshooting produksi dan diagnostik sisi pelanggan. Saya terus bertindak sebagai penasihat teknis kunci ketika masalah tidak dapat ditangani oleh teknisi lapangan, memberikan analisis akar masalah dan arahan solusi. Saya memiliki pemahaman mendalam tentang sistem kelistrikan aksesori dan terkait pembakaran, termasuk baterai, pengisian, CDI, booster, dan komponen pengapian. Ini mengurangi waktu eskalasi dan meningkatkan efisiensi troubleshooting.",
    skill1_2_title:
      "Rekayasa Kendaraan EV & ICE (Desain, Prototyping, Testing)",
    skill1_2_desc:
      "Berkontribusi pada pekerjaan rekayasa end-to-end untuk EV roda 3, mencakup desain, prototyping, testing, validasi, dan continuous improvement. Untuk platform EV, keterlibatan saya mencakup sistem head-to-toe, termasuk arsitektur elektrikal dan validasi fungsional. Kendaraan ini telah digunakan secara komersial dan mendukung bisnis dengan penjualan tahunan sekitar IDR 50 miliar, memastikan keandalan rekayasa selaras dengan penggunaan operasional nyata.",

    // Domain 2: Digitalization & System Development
    domain2_title: "Digitalisasi & Pengembangan Sistem",
    skill2_1_title: "Digitalisasi Manufaktur & Sistem Andon (IoT)",
    skill2_1_desc:
      "Mendukung lini produksi manufaktur dengan mengembangkan sistem Andon berbasis IoT untuk memantau masalah kualitas dan operasional secara real time. Sistem ini menerapkan 7 QC Tools seperti Diagram Fishbone, Diagram Scatter, dan Analisis Pareto untuk menyusun identifikasi masalah dan analisis akar penyebab. Ini meningkatkan transparansi produksi dan mengurangi waktu respons terhadap abnormalitas di shop floor.",
    skill2_2_title: "Tata Kelola Digitalisasi Perusahaan & Sistem Web Sales",
    skill2_2_desc:
      "Bertindak sebagai bagian dari tim digitalisasi yang bertanggung jawab mengevaluasi dan menyetujui inisiatif digitalisasi di empat unit bisnis. Peran saya memastikan kelayakan, keandalan sistem, dan tanggung jawab PIC yang jelas. Secara paralel, saya mengembangkan aplikasi web Operations One Solution menggunakan Laravel untuk menghubungkan dealer dan tim penjualan internal untuk bisnis 3W, memusatkan data dan meningkatkan kualitas insight. Proyek ekspansi besar direncanakan untuk 2026 dengan target meningkatkan volume penjualan hingga lima kali lipat.",

    // Domain 3: Data Analytics & Decision Support
    domain3_title: "Analitik Data & Dukungan Keputusan",
    skill3_1_title: "Analitik Excel Lanjutan & Dokumentasi ISO",
    skill3_1_desc:
      "Menerapkan teknik Excel lanjutan termasuk VLOOKUP, HLOOKUP, Pivot Tables, dan VBA Macros untuk analisis operasional dan dokumentasi standar seperti-ISO. Mengembangkan format data terstruktur dan file analitis yang meningkatkan konsistensi data, kesiapan audit, dan traceability di seluruh departemen.",
    skill3_2_title: "Analitik Perencanaan Produksi & Pelaporan Manajemen",
    skill3_2_desc:
      "Mengembangkan laporan harian Perencanaan Produksi vs Aktual yang mencakup lebih dari 20 jenis produk, memungkinkan manajemen memantau kinerja dan penyimpangan dengan jelas. Laporan ini mengubah data produksi mentah menjadi insight yang dapat ditindaklanjuti dan mendukung keputusan perencanaan yang lebih cepat. Python dan Power BI digunakan untuk meningkatkan skalabilitas pemrosesan data dan visualisasi.",

    // Domain 4: Marketing Analytics & Strategy
    domain4_title: "Analitik Marketing & Strategi",
    skill4_1_title: "Framework Strategi Marketing & One-Year Policy (OYP)",
    skill4_1_desc:
      "Mendukung divisi marketing dalam mengembangkan dokumen One-Year Policy (OYP) dan Annual Plan (AP) dengan menerapkan framework marketing terstruktur seperti Brand Awareness, CSAT, Customer Journey Mapping, 7P Analysis, dan Jobs To Be Done (JTBD). Konsep-konsep ini diterjemahkan ke dalam strategi yang dapat ditindaklanjuti selaras dengan eksekusi bisnis.",
    skill4_2_title: "Intelijen Pasar & Kompetitor (Data Skala Besar)",
    skill4_2_desc:
      "Melakukan analisis pasar dan kompetitor melalui data scraping dan riset, memproses lebih dari 100.000 catatan data. Insight mendukung keputusan manajemen terkait ekspansi pasar, strategi digital marketing, dan digitalisasi operasional. Data disusun dan divisualisasikan untuk dukungan keputusan tingkat eksekutif.",

    myPortfolio: "Portofolio Saya",
    allProjects: "Semua Proyek",
    digitalization: "Digitalisasi",
    dataAnalytics: "Analitik Data",
    webSystems: "Sistem Web",
    testimonials: "Testimoni",
    getInTouch: "Hubungi Saya",
    aboutSubtitle: "Mechatronics Engineer | Data & Digitalization Specialist",
    aboutDesc1:
      "Saya adalah Mechatronics Engineer dengan pengalaman profesional di operasi manufaktur, prototyping, testing, serta inisiatif digitalisasi lintas fungsi. Seiring waktu, jalur karier saya berkembang melampaui rekayasa tradisional menuju data analytics, system digitalization, dan marketing intelligence, yang memungkinkan saya menghubungkan aspek teknis dengan kebutuhan bisnis.",
    aboutDesc2:
      "Dalam ranah engineering, saya bekerja langsung dengan production support, PPIC, quality, dan testing, memastikan sistem berjalan stabil dan relevan di kondisi lapangan. Secara paralel, saya merancang dan mengimplementasikan digital solutions berbasis Laravel untuk menggantikan proses manual yang terfragmentasi—dengan fokus pada data structure, traceability, dan decision support.",
    aboutDesc3:
      "Di luar operasi internal, saya aktif mempelajari marketing analytics dan SEO, khususnya bagaimana Search Engine Result Page (SERP), interest over time, dan user behavior merefleksikan permintaan pasar yang nyata. Bagi saya, data marketing bukan hanya alat promosi, tetapi strategic input untuk product positioning, pricing, dan channel strategy.",
    aboutDesc4:
      "Arah profesional saya adalah menjadi hybrid contributor—seseorang yang mampu menjembatani engineering reality, data intelligence, dan market strategy ke dalam sistem yang praktis dan bisa digunakan.",
    name: "Nama:",
    role: "Peran:",
    roleValue: "Insinyur Mekatronika",
    email: "Email:",
    location: "Lokasi:",
    yearsExperience: "Tahun Pengalaman",
    projectsDelivered: "20+ Pekerjaan Selesai",
    coreDomains: "Domain Inti",
    careerHistory: "Riwayat Karir",
    career1: "Electrical Automotive Engineer",
    career2: "Product Performance Tester",
    career3: "Market Data Analyst",
    career4: "Operation Solution Developer",
    coreDomainsTitle: "Domain Inti",
    domain1: "Engineering & Manufacturing Systems",
    domain2: "Digitalization & System Development",
    domain3: "Data Analytics & Decision Support",
    domain4: "Marketing Analytics & Strategy",
  },
  en: {
    niceToMeet: "Nice to Meet You",
    aboutMe: "About Me",
    age: "Age:",
    residence: "Residence:",
    freelance: "Freelance:",
    available: "Available",
    address: "Address:",
    heroTitle:
      "Mechatronics Engineer | Data & Digitalization Specialist | Marketing Analytics",
    heroDesc1:
      "Mechatronics Engineer with 5+ years of hands-on experience across automotive engineering, product testing, data analysis, marketing, and business digitalization. I bridge engineering execution, data-driven insight, and digital systems to help organizations improve operational efficiency, visibility, and market performance.",
    heroDesc2:
      "With professional experience spanning manufacturing operations, prototyping, and cross-functional digitalization initiatives, I view problems from both technical and business perspectives. I develop web-based solutions using Laravel and analyze market trends through SEO and marketing analytics.",
    mySkills: "My Skills",
    skillsPortfolio: "Skills & Portfolio",

    // Domain 1: Engineering & Manufacturing
    domain1_title: "Engineering & Manufacturing",
    skill1_1_title:
      "Electrical System Architecture & Field Troubleshooting (3W ICE)",
    skill1_1_desc:
      "Led the breakdown and documentation of the complete electrical system of a 3-wheel ICE vehicle into a clear, easy-to-understand diagram used for field problem solving. The system supports both production troubleshooting and customer-side diagnostics. I continue to act as a key technical advisor when issues cannot be handled by field technicians, providing root-cause analysis and solution direction. I have deep understanding of accessory and combustion-related electrical systems, including battery, charging, CDI, booster, and ignition components. This reduced escalation time and improved troubleshooting efficiency.",
    skill1_2_title:
      "EV & ICE Vehicle Engineering (Design, Prototyping, Testing)",
    skill1_2_desc:
      "Contributed end-to-end engineering work for 3-wheel EV, covering design, prototyping, testing, validation, and continuous improvement. For EV platforms, my involvement covered head-to-toe systems, including electrical architecture and functional validation. These vehicles are commercially deployed and support a business with approximately IDR 50 billion in annual sales, ensuring engineering reliability aligns with real operational usage.",

    // Domain 2: Digitalization & System Development
    domain2_title: "Digitalization & System Development",
    skill2_1_title: "Manufacturing Digitalization & Andon System (IoT)",
    skill2_1_desc:
      "Supported manufacturing production line by developing an IoT-based Andon system to monitor quality and operational issues in real time. The system applied 7 QC Tools such as Fishbone Diagram, Scatter Diagram, and Pareto Analysis to structure problem identification and root-cause analysis. This improved production transparency and reduced response time to abnormalities on the shop floor.",
    skill2_2_title: "Company-wide Digitalization Governance & Sales Web System",
    skill2_2_desc:
      "Acted as part of a digitalization task force responsible for evaluating and approving digitalization initiatives across four business units. My role ensured feasibility, system reliability, and clear PIC responsibility. In parallel, I developed an Operations One Solution web application using Laravel to connect dealers and internal sales teams for the 3W business, centralizing data and improving insight quality. A major expansion project is planned for 2026 with a target to increase sales volume up to five times.",

    // Domain 3: Data Analytics & Decision Support
    domain3_title: "Data Analytics & Decision Support",
    skill3_1_title: "Advanced Excel Analytics & ISO Documentation",
    skill3_1_desc:
      "Applied advanced Excel techniques including VLOOKUP, HLOOKUP, Pivot Tables, and VBA Macros for operational analysis and ISO like-standard documentation. Developed structured data formats and analytical files that improved data consistency, audit readiness, and traceability across departments.",
    skill3_2_title: "Production Planning Analytics & Management Reporting",
    skill3_2_desc:
      "Developed a daily Production Planning vs Actual report covering more than 20 product types, enabling management to clearly monitor performance and deviations. The report transformed raw production data into actionable insight and supported faster planning decisions. Python and Power BI were used to improve data processing and visualization scalability.",

    // Domain 4: Marketing Analytics & Strategy
    domain4_title: "Marketing Analytics & Strategy",
    skill4_1_title: "Marketing Strategy Frameworks & One-Year Policy (OYP)",
    skill4_1_desc:
      "Supported the marketing division in developing One-Year Policy (OYP) and Annual Plan (AP) documents by applying structured marketing frameworks such as Brand Awareness, CSAT, Customer Journey Mapping, 7P Analysis, and Jobs To Be Done (JTBD). These concepts were translated into actionable strategies aligned with business execution.",
    skill4_2_title: "Market & Competitor Intelligence (Large-Scale Data)",
    skill4_2_desc:
      "Conducted market and competitor analysis through data scraping and research, processing more than 100,000 data records. Insights supported management decisions related to market expansion, digital marketing strategy, and operational digitalization. Data was structured and visualized for executive-level decision support.",

    myPortfolio: "My Portfolio",
    allProjects: "All Projects",
    digitalization: "Digitalization",
    dataAnalytics: "Data Analytics",
    webSystems: "Web Systems",
    testimonials: "Testimonials",
    getInTouch: "Get In Touch",
    aboutSubtitle: "Mechatronics Engineer | Data & Digitalization Specialist",
    aboutDesc1:
      "I am a Mechatronics Engineer with professional experience spanning manufacturing operations, prototyping, testing, and cross-functional digitalization initiatives. My career path has evolved beyond traditional engineering into data analytics, system digitalization, and marketing intelligence, allowing me to view problems from both technical and business perspectives.",
    aboutDesc2:
      "In engineering, I work hands-on with production support, PPIC, quality, and testing, ensuring systems function reliably in real-world conditions. In parallel, I design and implement digital solutions using Laravel to replace manual, fragmented processes—focusing on data structure, traceability, and decision support.",
    aboutDesc3:
      "Beyond internal operations, I actively study marketing analytics and SEO, particularly how Search Engine Result Pages (SERP), interest over time, and user behavior reflect real market demand. I analyze trends as strategic inputs for product positioning, pricing, and channel decisions.",
    aboutDesc4:
      "My professional direction is focused on becoming a hybrid contributor—someone who can connect engineering reality, data intelligence, and market strategy into cohesive systems.",
    name: "Name:",
    role: "Role:",
    roleValue: "Mechatronics Engineer",
    email: "Email:",
    location: "Location:",
    yearsExperience: "Years Experience",
    projectsDelivered: "20+ Jobs Done",
    coreDomains: "Core Domains",
    careerHistory: "Career History",
    career1: "Electrical Automotive Engineer",
    career2: "Product Performance Tester",
    career3: "Market Data Analyst",
    career4: "Operation Solution Developer",
    coreDomainsTitle: "Core Domains",
    domain1: "Engineering & Manufacturing Systems",
    domain2: "Digitalization & System Development",
    domain3: "Data Analytics & Decision Support",
    domain4: "Marketing Analytics & Strategy",
  },
};

let currentLang = localStorage.getItem("language") || "id";

function translatePage(lang) {
  currentLang = lang;
  localStorage.setItem("language", lang);

  // Update all elements with data-translate attribute
  document.querySelectorAll("[data-translate]").forEach((element) => {
    const key = element.getAttribute("data-translate");
    if (element && translations[lang] && translations[lang][key]) {
      element.textContent = translations[lang][key];
    }
  });

  // Update language button text
  const langText = document.querySelector(".lang-text");
  if (langText) {
    langText.textContent = lang === "id" ? "EN" : "ID";
  }

  // Update nav tooltips
  const navLinks = document.querySelectorAll(".nav-link");
  const tooltips = {
    id: {
      Home: "Beranda",
      About: "Tentang",
      Skills: "Keahlian",
      Portfolio: "Portofolio",
      Testimonials: "Testimoni",
      Contact: "Kontak",
      Beranda: "Beranda",
      Tentang: "Tentang",
      Keahlian: "Keahlian",
      Portofolio: "Portofolio",
      Testimoni: "Testimoni",
      Kontak: "Kontak",
    },
    en: {
      Home: "Home",
      About: "About",
      Skills: "Skills",
      Portfolio: "Portfolio",
      Testimonials: "Testimonials",
      Contact: "Contact",
      Beranda: "Home",
      Tentang: "About",
      Keahlian: "Skills",
      Portofolio: "Portfolio",
      Testimoni: "Testimonials",
      Kontak: "Contact",
    },
  };

  navLinks.forEach((link) => {
    const currentTitle = link.getAttribute("data-title");
    if (
      link &&
      currentTitle &&
      tooltips[lang] &&
      tooltips[lang][currentTitle]
    ) {
      link.setAttribute("data-title", tooltips[lang][currentTitle]);
    }
  });
}

// Initialize language on page load
document.addEventListener("DOMContentLoaded", function () {
  translatePage(currentLang);

  // Language toggle button
  const languageToggle = document.getElementById("languageToggle");
  if (languageToggle) {
    languageToggle.addEventListener("click", function () {
      const newLang = currentLang === "id" ? "en" : "id";
      translatePage(newLang);
    });
  }
});

// ============================================
// 1. INITIALIZE AOS (Animate On Scroll)
// ============================================
document.addEventListener("DOMContentLoaded", function () {
  AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true,
    offset: 100,
  });
});

// ============================================
// 2. NAVIGATION - Sticky Navbar & Mobile Menu
// ============================================
const navbar = document.getElementById("navbar");
const hamburger = document.getElementById("hamburger");
const navMenu = document.getElementById("navMenu");
const navLinks = document.querySelectorAll(".nav-link");

// Sticky navbar on scroll
window.addEventListener("scroll", function () {
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// Mobile menu toggle
hamburger.addEventListener("click", function () {
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
});

// Language toggle also closes mobile menu
const languageToggle = document.getElementById("languageToggle");
if (languageToggle) {
  languageToggle.addEventListener("click", function () {
    // Close mobile menu if open
    if (navMenu.classList.contains("active")) {
      hamburger.classList.remove("active");
      navMenu.classList.remove("active");
    }
  });
}

// Close mobile menu when clicking nav links
navLinks.forEach((link) => {
  link.addEventListener("click", function () {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
  });
});

// ============================================
// 3. SMOOTH SCROLLING for Navigation Links
// ============================================
navLinks.forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    const targetId = this.getAttribute("href");
    const targetSection = document.querySelector(targetId);

    if (targetSection) {
      const offsetTop = targetSection.offsetTop - 70; // Account for fixed navbar
      window.scrollTo({
        top: offsetTop,
        behavior: "smooth",
      });
    }
  });
});

// ============================================
// 4. HERO TYPEWRITER EFFECT
// ============================================
const typewriterElement = document.getElementById("typewriter");
const texts = [
  "Mechatronics Engineer",
  "Data & Digitalization Specialist",
  "Marketing Analytics",
  "Laravel Web Developer",
];
let textIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingSpeed = 100;

function typeWriter() {
  if (!typewriterElement) return;

  const currentText = texts[textIndex];

  if (isDeleting) {
    typewriterElement.textContent = currentText.substring(0, charIndex - 1);
    charIndex--;
    typingSpeed = 50;
  } else {
    typewriterElement.textContent = currentText.substring(0, charIndex + 1);
    charIndex++;
    typingSpeed = 100;
  }

  if (!isDeleting && charIndex === currentText.length) {
    // Pause at end of text
    typingSpeed = 2000;
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    textIndex = (textIndex + 1) % texts.length;
    typingSpeed = 500;
  }

  setTimeout(typeWriter, typingSpeed);
}

// Start typewriter effect when page loads
window.addEventListener("load", function () {
  if (typewriterElement) {
    setTimeout(typeWriter, 1000);
  }
});

// ============================================
// 5. COUNTER ANIMATION for About Stats
// ============================================
const counters = document.querySelectorAll(".counter");
let counterAnimated = false;

function animateCounters() {
  counters.forEach((counter) => {
    if (!counter) return;

    const target = parseFloat(counter.getAttribute("data-target"));
    const increment = target / 100;
    let current = 0;

    const updateCounter = () => {
      if (current < target) {
        current += increment;
        if (target % 1 !== 0) {
          counter.textContent = current.toFixed(1);
        } else {
          counter.textContent = Math.ceil(current);
        }
        setTimeout(updateCounter, 20);
      } else {
        if (target % 1 !== 0) {
          counter.textContent = target.toFixed(1);
        } else {
          counter.textContent = target;
        }
      }
    };

    updateCounter();
  });
}

// Trigger counter animation when About section is in view
window.addEventListener("scroll", function () {
  if (!counterAnimated) {
    const aboutSection = document.querySelector(".about-section");
    if (aboutSection) {
      const aboutPosition = aboutSection.getBoundingClientRect().top;
      const screenPosition = window.innerHeight / 1.3;

      if (aboutPosition < screenPosition) {
        animateCounters();
        counterAnimated = true;
      }
    }
  }
});

// ============================================
// 6. SKILLS - Animated Progress Bars
// ============================================
const skillsSection = document.querySelector(".skills-section");
let skillsAnimated = false;

function animateSkills() {
  const skillBars = document.querySelectorAll(".skill-progress");
  skillBars.forEach((bar) => {
    const progress = bar.getAttribute("data-progress");
    bar.style.width = progress + "%";
  });
}

window.addEventListener("scroll", function () {
  if (!skillsAnimated && skillsSection) {
    const skillsPosition = skillsSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.3;

    if (skillsPosition < screenPosition) {
      animateSkills();
      skillsAnimated = true;
    }
  }
});

// ============================================
// 7. PORTFOLIO - Filter Functionality
// ============================================
const filterBtns = document.querySelectorAll(".filter-btn");
const portfolioItems = document.querySelectorAll(".portfolio-item");

filterBtns.forEach((btn) => {
  btn.addEventListener("click", function () {
    // Remove active class from all buttons
    filterBtns.forEach((b) => b.classList.remove("active"));
    // Add active class to clicked button
    this.classList.add("active");

    const filterValue = this.getAttribute("data-filter");

    portfolioItems.forEach((item) => {
      if (
        filterValue === "all" ||
        item.getAttribute("data-category") === filterValue
      ) {
        item.style.display = "block";
        setTimeout(() => {
          item.style.opacity = "1";
          item.style.transform = "scale(1)";
        }, 10);
      } else {
        item.style.opacity = "0";
        item.style.transform = "scale(0.8)";
        setTimeout(() => {
          item.style.display = "none";
        }, 300);
      }
    });
  });
});

// ============================================
// 8. LIGHTBOX for Portfolio Images
// ============================================
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const lightboxClose = document.querySelector(".lightbox-close");
const portfolioLinks = document.querySelectorAll("[data-lightbox]");

portfolioLinks.forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    const imgSrc = this.closest(".portfolio-item").querySelector("img").src;
    lightboxImg.src = imgSrc;
    lightbox.classList.add("active");
  });
});

lightboxClose.addEventListener("click", function () {
  lightbox.classList.remove("active");
});

lightbox.addEventListener("click", function (e) {
  if (e.target === lightbox) {
    lightbox.classList.remove("active");
  }
});

// Close lightbox with Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && lightbox.classList.contains("active")) {
    lightbox.classList.remove("active");
  }
});

// ============================================
// 9. TESTIMONIALS SLIDER
// ============================================
const testimonialItems = document.querySelectorAll(".testimonial-item");
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");
const dots = document.querySelectorAll(".testimonial-dots .dot");
let currentSlide = 0;

// Only run testimonials slider if elements exist
if (testimonialItems.length > 0) {
  function showTestimonial(index) {
    // Remove active class from all items and dots
    testimonialItems.forEach((item) => item.classList.remove("active"));
    dots.forEach((dot) => dot.classList.remove("active"));

    // Add active class to current item and dot
    testimonialItems[index].classList.add("active");
    dots[index].classList.add("active");
  }

  function nextTestimonial() {
    currentSlide = (currentSlide + 1) % testimonialItems.length;
    showTestimonial(currentSlide);
  }

  function prevTestimonial() {
    currentSlide =
      (currentSlide - 1 + testimonialItems.length) % testimonialItems.length;
    showTestimonial(currentSlide);
  }

  if (nextBtn && prevBtn) {
    nextBtn.addEventListener("click", nextTestimonial);
    prevBtn.addEventListener("click", prevTestimonial);
  }

  // Dots navigation
  dots.forEach((dot, index) => {
    dot.addEventListener("click", function () {
      currentSlide = index;
      showTestimonial(currentSlide);
    });
  });

  // Auto-play testimonials (optional)
  let testimonialInterval = setInterval(nextTestimonial, 5000);

  // Pause auto-play on hover
  const testimonialsSlider = document.querySelector(".testimonials-slider");
  if (testimonialsSlider) {
    testimonialsSlider.addEventListener("mouseenter", function () {
      clearInterval(testimonialInterval);
    });

    testimonialsSlider.addEventListener("mouseleave", function () {
      testimonialInterval = setInterval(nextTestimonial, 5000);
    });
  }
}

// ============================================
// 10. CONTACT FORM - Validation & Submission
// ============================================
const contactForm = document.getElementById("contactForm");
const formGroups = document.querySelectorAll(".form-group");

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

function showError(input, message) {
  const formGroup = input.parentElement;
  const errorMsg = formGroup.querySelector(".error-message");
  if (!errorMsg) return;

  formGroup.classList.add("error");
  errorMsg.textContent = message;
  errorMsg.style.display = "block";
}

function clearError(input) {
  const formGroup = input.parentElement;
  const errorMsg = formGroup.querySelector(".error-message");
  formGroup.classList.remove("error");
  errorMsg.style.display = "none";
}

function validateForm() {
  let isValid = true;

  // Clear all previous errors
  formGroups.forEach((group) => {
    const input = group.querySelector("input, textarea");
    if (input) clearError(input);
  });

  // Validate name
  const nameInput = document.getElementById("name");
  if (nameInput.value.trim() === "") {
    showError(nameInput, "Name is required");
    isValid = false;
  } else if (nameInput.value.trim().length < 2) {
    showError(nameInput, "Name must be at least 2 characters");
    isValid = false;
  }

  // Validate email
  const emailInput = document.getElementById("email");
  if (emailInput.value.trim() === "") {
    showError(emailInput, "Email is required");
    isValid = false;
  } else if (!validateEmail(emailInput.value)) {
    showError(emailInput, "Please enter a valid email");
    isValid = false;
  }

  // Validate subject
  const subjectInput = document.getElementById("subject");
  if (subjectInput.value.trim() === "") {
    showError(subjectInput, "Subject is required");
    isValid = false;
  }

  // Validate message
  const messageInput = document.getElementById("message");
  if (messageInput.value.trim() === "") {
    showError(messageInput, "Message is required");
    isValid = false;
  } else if (messageInput.value.trim().length < 10) {
    showError(messageInput, "Message must be at least 10 characters");
    isValid = false;
  }

  return isValid;
}

// Initialize EmailJS with your public key
(function () {
  emailjs.init({
    publicKey: "11l-lsn2TAzgMw_o1", // Replace with your EmailJS public key
  });
})();

if (contactForm) {
  contactForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (validateForm()) {
      // Show loading state
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const btnText = submitBtn.querySelector(".btn-text");
      const btnLoader = submitBtn.querySelector(".btn-loader");

      btnText.style.display = "none";
      btnLoader.style.display = "inline-block";
      submitBtn.disabled = true;

      // Send email using EmailJS
      const templateParams = {
        title: document.getElementById("subject").value,
        name: document.getElementById("name").value,
        time: new Date().toLocaleString("id-ID", {
          dateStyle: "full",
          timeStyle: "short",
        }),
        message: document.getElementById("message").value,
        email: document.getElementById("email").value,
      };

      emailjs.send("service_ctrclcn", "template_fzkgi64", templateParams).then(
        function (response) {
          // Reset button state
          btnText.style.display = "inline-block";
          btnLoader.style.display = "none";
          submitBtn.disabled = false;

          // Show success message
          const formResponse = document.querySelector(".form-response");
          if (formResponse) {
            formResponse.className = "form-response success";
            formResponse.textContent =
              "Thank you! Your message has been sent successfully.";

            // Reset form
            contactForm.reset();

            // Hide success message after 5 seconds
            setTimeout(() => {
              formResponse.style.display = "none";
            }, 5000);
          }
        },
        function (error) {
          // Reset button state
          btnText.style.display = "inline-block";
          btnLoader.style.display = "none";
          submitBtn.disabled = false;

          // Show error message
          const formResponse = document.querySelector(".form-response");
          if (formResponse) {
            formResponse.className = "form-response error";
            formResponse.textContent =
              "Sorry, there was an error sending your message. Please try again.";

            // Hide error message after 5 seconds
            setTimeout(() => {
              formResponse.style.display = "none";
            }, 5000);
          }
        }
      );
    }
  });

  // Real-time validation on input
  const inputs = contactForm.querySelectorAll("input, textarea");
  inputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (this.value.trim() !== "") {
        clearError(this);
      }
    });
  });
}

// ============================================
// 11. PARALLAX EFFECT for Hero Background
// ============================================
window.addEventListener("scroll", function () {
  const scrolled = window.pageYOffset;
  const heroSection = document.querySelector(".hero-section");

  if (heroSection) {
    const parallax = heroSection.querySelector("::before");
    // Parallax effect is handled by CSS background-attachment: fixed
  }
});

// ============================================
// 12. SCROLL REVEAL for Active Nav Links
// ============================================
window.addEventListener("scroll", function () {
  let current = "";
  const sections = document.querySelectorAll("section");

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;

    if (pageYOffset >= sectionTop - 200) {
      current = section.getAttribute("id");
    }
  });

  navLinks.forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
});

// ============================================
// 13. PERFORMANCE OPTIMIZATIONS
// ============================================

// Lazy load images
if ("IntersectionObserver" in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute("data-src");
        }
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll("img[data-src]").forEach((img) => {
    imageObserver.observe(img);
  });
}

// ============================================
// 14. CONSOLE MESSAGE (Optional)
// ============================================
console.log(
  "%c👋 Welcome to Reyza's Portfolio!",
  "color: #007bff; font-size: 20px; font-weight: bold;"
);
console.log(
  "%cInterested in the code? Let's connect!",
  "color: #6c757d; font-size: 14px;"
);

// ============================================
// 15. PREVENT LOADING FLASH
// ============================================
window.addEventListener("load", function () {
  document.body.classList.remove("loading");
});
