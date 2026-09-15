"""PowerSync feature explorer page, built in English and Indonesian.

Source: the PowerSync requirements spec (RFP + SRS, July 2026). Every module has routes in
the live codebase; features tagged spec=True are optional spec items not confirmed in the build.
All text is bilingual inline as (english, indonesian). Called from build.py for each language.
"""

SPEC = ("Spec item, not confirmed in the build", "Item spec, belum terkonfirmasi di build")


def F(name, does, solves, spec=False):
    return {"name": name, "does": does, "solves": solves, "spec": spec}


CLUSTERS = [
    {"id": "core", "letter": "A", "name": ("Core transactions", "Transaksi inti"),
     "desc": ("From a dealer's order to a delivered, paid and registered unit.", "Dari order dealer sampai unit terkirim, terbayar, dan teregistrasi.")},
    {"id": "parts", "letter": "B", "name": ("Spare parts", "Spare parts"),
     "desc": ("Catalogue, ordering and stock for parts.", "Katalog, order, dan stok spare parts.")},
    {"id": "internal", "letter": "C", "name": ("Manufacturing & internal work", "Manufaktur & kerja internal"),
     "desc": ("Production planning plus the projects and meetings around it.", "Perencanaan produksi serta project dan meeting di sekitarnya.")},
    {"id": "marketing", "letter": "D", "name": ("Dealer marketing", "Marketing dealer"),
     "desc": ("Events, materials, rewards, content and surveys for dealers.", "Event, material, reward, konten, dan survei untuk dealer.")},
    {"id": "platform", "letter": "E", "name": ("Platform & governance", "Platform & tata kelola"),
     "desc": ("Who can see what, and what changed.", "Siapa bisa melihat apa, dan apa yang berubah.")},
    {"id": "floor", "letter": "F", "name": ("Shop floor & analytics", "Shop floor & analitik"),
     "desc": ("Kiosks, daily production reports, internal QC and the customer database.", "Kiosk, laporan produksi harian, internal QC, dan database customer.")},
]

MODULES = [
    {
        "id": "order", "no": 1, "cluster": "core",
        "name": ("Order Management", "Order Management"),
        "what": ("Dealer vehicle orders, from pending to complete.", "Order kendaraan dealer, dari pending sampai complete."),
        "solves": ("Orders sent by letter, email and WhatsApp with no shared status and no record of who approved what.",
                   "Order yang dikirim lewat surat, email, dan WhatsApp tanpa status bersama dan tanpa catatan siapa yang meng-approve."),
        "features": [
            F(("Order with unit configuration", "Order dengan konfigurasi unit"),
              ("A dealer orders one or more units and picks base, body, cabin, colour and accessories.", "Dealer memesan satu unit atau lebih dan memilih base, body, cabin, warna, dan aksesori."),
              ("Invalid combinations get blocked at entry instead of being found at the factory.", "Kombinasi yang tidak valid langsung ditolak saat input, bukan baru ketahuan di pabrik.")),
            F(("Ten statuses with permissions", "10 status dengan permission"),
              ("Pending, received, approved, confirmed, processed, delivered, billed, complete, plus cancelled. Each move needs the right permission.", "Pending, received, approved, confirmed, processed, delivered, billed, complete, plus cancelled. Setiap perpindahan status butuh permission yang sesuai."),
              ("Nobody can skip a step, such as jumping from pending straight to delivered.", "Tidak ada yang bisa melompati tahap, misalnya dari pending langsung ke delivered.")),
            F(("Audit trail and notifications", "Audit trail dan notifikasi"),
              ("Every status change records old and new values, user and time, and notifies the people involved.", "Setiap perubahan status mencatat nilai lama dan baru, user, dan waktu, lalu memberi notifikasi ke pihak terkait."),
              ("Arguments about who changed an order can be settled from the log.", "Perdebatan soal siapa yang mengubah order bisa dijawab dari log.")),
            F(("Delivery address by region", "Alamat kirim per wilayah"),
              ("Province, city and district dropdowns built on Indonesian region data.", "Dropdown provinsi, kota, dan kecamatan dari data wilayah Indonesia."),
              ("Address typos that break delivery and registration documents.", "Salah ketik alamat yang merusak dokumen pengiriman dan registrasi.")),
        ],
        "links": ["unit_master", "qi", "delivery_prep", "billing", "legal", "rbac"],
    },
    {
        "id": "qi", "no": 2, "cluster": "core",
        "name": ("Pre-delivery Quality Inspection", "Quality Inspection pra-pengiriman"),
        "what": ("An 85+ point checklist for every unit before it ships.", "Checklist 85+ titik untuk setiap unit sebelum dikirim."),
        "solves": ("Defects found by the dealer after delivery, with no proof of the unit's condition when it left.",
                   "Cacat yang baru ditemukan dealer setelah unit dikirim, tanpa bukti kondisi unit saat keluar pabrik."),
        "features": [
            F(("Checklist by category and part", "Checklist per kategori dan komponen"),
              ("Each unit is checked part by part as OK, NG or N/A, with notes and photos.", "Setiap unit dicek per komponen: OK, NG, atau N/A, dengan catatan dan foto."),
              ("Inspections that depended on memory and paper forms.", "Inspeksi yang bergantung pada ingatan dan formulir kertas.")),
            F(("NG with photo proof", "NG dengan bukti foto"),
              ("A part marked NG needs a defect category and at least one photo.", "Komponen yang ditandai NG wajib punya kategori defect dan minimal satu foto."),
              ("Arguments later about whether a defect was there before shipping.", "Perdebatan belakangan soal apakah cacat sudah ada sebelum dikirim.")),
            F(("Completion rules", "Aturan penyelesaian"),
              ("An inspection can only finish when every part is classified, and a finished inspection can't be edited.", "Inspeksi hanya bisa selesai kalau semua komponen sudah diklasifikasi, dan inspeksi yang selesai tidak bisa diubah."),
              ("Half-filled checklists and results changed after the fact.", "Checklist setengah terisi dan hasil yang diubah belakangan.")),
            F(("Inspection report PDF", "Report inspeksi PDF"),
              ("Generates a report with the full checklist, NG photos and the inspector's signature.", "Membuat report berisi checklist lengkap, foto NG, dan tanda tangan inspector."),
              ("Re-typing results into a document for the dealer.", "Mengetik ulang hasil inspeksi ke dokumen untuk dealer.")),
        ],
        "links": ["order", "delivery_claims", "delivery_prep", "internal_qc"],
    },
    {
        "id": "delivery_claims", "no": 3, "cluster": "core",
        "name": ("Delivery Claims", "Delivery Claims"),
        "what": ("Claims for damage or missing items when a dealer receives a unit.", "Klaim kerusakan atau kekurangan saat dealer menerima unit."),
        "solves": ("Delivery complaints sent as photos in chat, with no status and no link to what inspection found.",
                   "Komplain pengiriman yang dikirim sebagai foto di chat, tanpa status dan tanpa kaitan ke hasil inspeksi."),
        "features": [
            F(("Claim with photo evidence", "Klaim dengan bukti foto"),
              ("The dealer files a claim on a delivered order with type, description, photos and value.", "Dealer mengajukan klaim atas order yang sudah delivered, lengkap dengan jenis, deskripsi, foto, dan nilai klaim."),
              ("Missing details that slow the review down.", "Detail yang kurang sehingga review jadi lambat.")),
            F(("Linked to inspection findings", "Terhubung ke temuan inspeksi"),
              ("A claim can link to the NG parts recorded in the pre-delivery inspection.", "Klaim bisa dihubungkan ke komponen NG yang tercatat di inspeksi pra-pengiriman."),
              ("Reviewing a claim without knowing what the factory already saw.", "Me-review klaim tanpa tahu apa yang sudah terlihat di pabrik.")),
            F(("Review workflow with a time window", "Workflow review dengan batas waktu"),
              ("Submitted, under review, approved or rejected, resolved. Claims are accepted only for a set period after delivery.", "Submitted, under review, approved atau rejected, resolved. Klaim hanya diterima dalam periode tertentu setelah delivery."),
              ("Late claims, and approved claims being reversed.", "Klaim yang terlambat, dan klaim approved yang dibatalkan lagi.")),
            F(("Bulk review", "Review massal"),
              ("Approve or reject several claims at once with a shared comment.", "Approve atau reject beberapa klaim sekaligus dengan komentar yang sama."),
              ("Handling claims one by one when many units arrive together.", "Menangani klaim satu per satu saat banyak unit datang bersamaan.")),
        ],
        "links": ["qi", "order", "ksg"],
    },
    {
        "id": "ksg", "no": 4, "cluster": "core",
        "name": ("KSG Warranty Claims", "KSG Warranty Claims"),
        "what": ("Free-service and warranty claims per unit, with a QC review.", "Klaim servis gratis dan garansi per unit, dengan review QC."),
        "solves": ("Quarterly batches of paper coupons reconciled by hand in Excel.",
                   "Kupon kertas yang dikumpulkan per kuartal lalu dicocokkan manual di Excel."),
        "features": [
            F(("Warranty period from the delivery date", "Masa garansi dari tanggal delivery"),
              ("The warranty window is worked out from the delivery date, 12 months by default.", "Masa garansi dihitung dari tanggal delivery, default 12 bulan."),
              ("Claims approved for units already out of warranty.", "Klaim yang di-approve untuk unit yang sudah lewat masa garansi.")),
            F(("Evidence on every claim", "Bukti di setiap klaim"),
              ("Photos, short videos and documents are attached to each claim, including mileage and a speedometer photo.", "Foto, video pendek, dan dokumen dilampirkan di setiap klaim, termasuk kilometer dan foto speedometer."),
              ("Claims nobody could check because the proof lived on someone's phone.", "Klaim yang tidak bisa dicek karena buktinya tersimpan di HP seseorang.")),
            F(("QC review through to replacement", "Review QC sampai replacement"),
              ("Draft, submitted, QC review, approved, replacement processed, closed. An approved replacement creates a linked replacement order.", "Draft, submitted, QC review, approved, replacement processed, closed. Replacement yang di-approve membuat order pengganti yang terhubung."),
              ("Replacements promised but never tracked as an order.", "Replacement yang dijanjikan tapi tidak pernah tercatat sebagai order.")),
            F(("Bulk creation and defect reports", "Bulk create dan report defect"),
              ("Create many claims from an Excel template; monthly, quarterly and yearly reports by defect type.", "Membuat banyak klaim dari template Excel; report bulanan, kuartalan, dan tahunan per jenis defect."),
              ("No view of which defects keep coming back.", "Tidak ada gambaran defect mana yang terus berulang.")),
        ],
        "links": ["order", "delivery_claims", "internal_qc"],
    },
    {
        "id": "part_claims", "no": 5, "cluster": "core",
        "name": ("Spare Parts Claims", "Spare Parts Claims"),
        "what": ("Claims for defective spare parts a dealer ordered.", "Klaim untuk spare parts cacat yang dipesan dealer."),
        "solves": ("Defective parts sent back with no record of where they are in repair.",
                   "Spare parts cacat yang dikembalikan tanpa catatan posisinya di proses repair."),
        "features": [
            F(("Claim against a delivered parts order", "Klaim atas order spare parts yang sudah dikirim"),
              ("The dealer claims against a spare parts order that was delivered.", "Dealer mengajukan klaim atas order spare parts yang sudah dikirim."),
              ("Claims that can't be matched to what was actually sold.", "Klaim yang tidak bisa dicocokkan dengan barang yang benar-benar dijual.")),
            F(("QC repair stages", "Tahap repair QC"),
              ("Received, under QC, repair in progress, repaired, delivered back, with evidence at each stage.", "Received, under QC, repair in progress, repaired, delivered back, dengan bukti di setiap tahap."),
              ("Dealers phoning to ask where their part is.", "Dealer yang menelepon untuk menanyakan di mana part mereka.")),
            F(("Repair history per item", "Riwayat repair per item"),
              ("Keeps the QC repair history of every claimed item.", "Menyimpan riwayat repair QC untuk setiap item yang diklaim."),
              ("Losing track of parts that fail more than once.", "Kehilangan jejak part yang rusak lebih dari sekali.")),
        ],
        "links": ["parts", "internal_qc"],
    },
    {
        "id": "vin", "no": 6, "cluster": "core",
        "name": ("VIN / Production Tracker", "VIN / Production Tracker"),
        "what": ("Chassis and engine numbers tracked per unit through production.", "Nomor rangka dan mesin dilacak per unit sepanjang produksi."),
        "solves": ("Numbers planned in spreadsheets and found wrong on invoices or registration papers.",
                   "Nomor yang direncanakan di spreadsheet dan baru ketahuan salah di invoice atau dokumen registrasi."),
        "features": [
            F(("Assign numbers one by one or in bulk", "Assign nomor satuan atau bulk"),
              ("Chassis and engine numbers go to order items individually or from an Excel upload.", "Nomor rangka dan mesin di-assign ke item order satu per satu atau lewat upload Excel."),
              ("Copy-paste errors when numbers move between files.", "Error copy-paste saat nomor dipindah antar file.")),
            F(("One number, one unit", "Satu nomor, satu unit"),
              ("A number can belong to only one order item, and it can't be released once the unit has shipped.", "Satu nomor hanya boleh terikat ke satu item order, dan tidak bisa dilepas setelah unit dikirim."),
              ("Duplicate numbers reaching delivery and registration.", "Nomor duplikat yang lolos sampai delivery dan registrasi.")),
            F(("Problem flags", "Flag masalah"),
              ("Numbers that look duplicated or mismatched get flagged for review.", "Nomor yang terlihat duplikat atau tidak cocok ditandai untuk di-review."),
              ("Errors noticed only when a customer's documents come back wrong.", "Error yang baru disadari saat dokumen customer kembali dalam kondisi salah.")),
            F(("Read numbers from a photo", "Baca nomor dari foto"),
              ("OCR reads the chassis or engine number from a photo.", "OCR membaca nomor rangka atau mesin dari foto."),
              ("Typing long numbers by hand on the production floor.", "Mengetik nomor panjang secara manual di lantai produksi.")),
        ],
        "links": ["order", "mes", "ppic", "legal"],
    },
    {
        "id": "unit_master", "no": 7, "cluster": "core",
        "name": ("Inventory & Unit Master", "Inventory & Unit Master"),
        "what": ("Master data for models: base, body, cabin, colour, accessories and images.", "Master data model: base, body, cabin, warna, aksesori, dan gambar."),
        "solves": ("Every team keeping its own version of what can be ordered.",
                   "Setiap tim menyimpan versinya sendiri tentang apa yang bisa dipesan."),
        "features": [
            F(("Configuration master", "Master konfigurasi"),
              ("One place to maintain units, bases, bodies, cabins, colours and accessories, with image galleries.", "Satu tempat untuk mengelola unit, base, body, cabin, warna, dan aksesori, lengkap dengan galeri gambar."),
              ("Dealers ordering combinations that no longer exist.", "Dealer memesan kombinasi yang sudah tidak tersedia.")),
            F(("Compatibility rules", "Aturan kompatibilitas"),
              ("Defines which base works with which body and cabin.", "Menentukan base mana yang cocok dengan body dan cabin mana."),
              ("Orders that can't be built as configured.", "Order yang tidak bisa diproduksi sesuai konfigurasinya.")),
            F(("Dealer-specific pricing", "Harga khusus per dealer"),
              ("Price tiers per unit, with special prices for particular dealers.", "Tier harga per unit, dengan harga khusus untuk dealer tertentu."),
              ("Price lists sent separately to each dealer and going out of date.", "Daftar harga yang dikirim terpisah ke setiap dealer lalu jadi tidak update.")),
            F(("Bulk import and export", "Bulk import dan export"),
              ("Master data can be loaded or exported through Excel.", "Master data bisa dimasukkan atau di-export lewat Excel."),
              ("Setting up a new model record by record.", "Menyiapkan model baru satu per satu.")),
        ],
        "links": ["order", "parts"],
    },
    {
        "id": "delivery_prep", "no": 8, "cluster": "core",
        "name": ("Delivery Preparation", "Delivery Preparation"),
        "what": ("Everything a unit needs before it can ship.", "Semua yang dibutuhkan unit sebelum bisa dikirim."),
        "solves": ("Units leaving the factory with documents missing.", "Unit keluar pabrik dengan dokumen yang belum lengkap."),
        "features": [
            F(("Travel documents and transport photos", "Dokumen perjalanan dan foto angkutan"),
              ("Upload travel permits, insurance and photos of the carrier truck.", "Upload surat jalan, asuransi, dan foto truk pengangkut."),
              ("No proof of how and when a unit left.", "Tidak ada bukti bagaimana dan kapan unit berangkat.")),
            F(("Delivery note numbers", "Nomor delivery note"),
              ("Delivery note numbers are generated in a set format.", "Nomor delivery note dibuat otomatis dengan format yang ditentukan."),
              ("Duplicate or skipped note numbers.", "Nomor surat jalan yang dobel atau terlewat.")),
            F(("PDI and number check per unit", "PDI dan cek nomor per unit"),
              ("Each unit gets its PDI document and a confirmed chassis and engine number.", "Setiap unit punya dokumen PDI serta konfirmasi nomor rangka dan mesin."),
              ("Shipping a unit whose numbers don't match its papers.", "Mengirim unit yang nomornya tidak cocok dengan dokumennya.")),
            F(("Delivery gate", "Gerbang delivery"),
              ("An order can't be marked delivered until preparation is complete and inspection is done.", "Order tidak bisa ditandai delivered sebelum persiapan lengkap dan inspeksi selesai."),
              ("A delivered status while paperwork is still open.", "Status sudah delivered padahal dokumennya belum beres.")),
        ],
        "links": ["order", "qi", "vin", "elhp"],
    },
    {
        "id": "legal", "no": 9, "cluster": "core",
        "name": ("Legal Request (vehicle registration)", "Legal Request (registrasi kendaraan)"),
        "what": ("Registration paperwork per unit: faktur, BBN, NIK and supporting IDs.", "Dokumen registrasi per unit: faktur, BBN, NIK, dan identitas pendukung."),
        "solves": ("Faktur requests in Excel, re-typed by admins before a paid registration step.",
                   "Pengajuan faktur di Excel yang diketik ulang admin sebelum tahap registrasi yang berbayar."),
        "features": [
            F(("Request tied to a chassis number", "Pengajuan terikat nomor rangka"),
              ("Each request is linked to one order item's chassis number, with vehicle and owner data.", "Setiap pengajuan terhubung ke nomor rangka satu item order, lengkap dengan data kendaraan dan pemilik."),
              ("Documents issued for the wrong unit.", "Dokumen yang terbit untuk unit yang salah.")),
            F(("ID upload with checks", "Upload identitas dengan validasi"),
              ("KTP and supporting photos are checked for format and size on upload.", "KTP dan foto pendukung dicek format dan ukurannya saat upload."),
              ("Unreadable or missing ID copies found late.", "Salinan identitas yang buram atau hilang baru ketahuan belakangan.")),
            F(("Bulk print on blank forms", "Bulk print di blanko"),
              ("Prints faktur and registration documents in bulk, with print positions you can adjust to pre-printed forms.", "Mencetak faktur dan dokumen registrasi secara massal, dengan posisi cetak yang bisa disesuaikan ke blanko."),
              ("Printing and aligning each document by hand.", "Mencetak dan menyesuaikan posisi dokumen satu per satu.")),
            F(("Faktur only after completion", "Faktur setelah complete"),
              ("A BBN faktur can be printed only after the order is complete.", "BBN faktur hanya bisa dicetak setelah order berstatus complete."),
              ("Registration starting before the sale is closed.", "Registrasi dimulai sebelum penjualan selesai.")),
        ],
        "links": ["order", "vin", "customers", "billing"],
    },
    {
        "id": "billing", "no": 10, "cluster": "core",
        "name": ("Billing & Payment", "Billing & Payment"),
        "what": ("Payment proof, confirmation, invoices and reconciliation.", "Bukti bayar, konfirmasi, invoice, dan rekonsiliasi."),
        "solves": ("Transfer receipts sent by chat and matched to orders by hand.", "Bukti transfer yang dikirim lewat chat lalu dicocokkan manual ke order."),
        "features": [
            F(("Payment proof upload", "Upload bukti bayar"),
              ("The dealer uploads a transfer receipt per order or per invoice.", "Dealer upload bukti transfer per order atau per invoice."),
              ("Receipts buried in chat history.", "Bukti transfer yang tenggelam di riwayat chat.")),
            F(("Verification before billing", "Verifikasi sebelum billing"),
              ("Submitted, verified, confirmed or rejected. An order can only be billed with confirmed proof.", "Submitted, verified, confirmed atau rejected. Order hanya bisa di-bill kalau bukti bayar sudah dikonfirmasi."),
              ("Units treated as paid before finance checked.", "Unit dianggap lunas sebelum finance mengecek.")),
            F(("Invoice PDF", "Invoice PDF"),
              ("Invoices with logo, items, tax, total and the amount written out in Indonesian.", "Invoice dengan logo, item, pajak, total, dan terbilang dalam bahasa Indonesia."),
              ("Invoices built by hand in Word or Excel.", "Invoice yang dibuat manual di Word atau Excel.")),
            F(("Billing dashboard", "Dashboard billing"),
              ("Pending, partial, paid and overdue at a glance, with daily to monthly exports.", "Pending, partial, paid, dan overdue dalam satu tampilan, dengan export harian sampai bulanan."),
              ("No quick answer to who still owes what.", "Tidak ada jawaban cepat soal siapa yang masih punya tagihan.")),
        ],
        "links": ["order", "legal", "parts"],
    },
    {
        "id": "parts", "no": 11, "cluster": "parts",
        "name": ("Spare Parts Ecosystem", "Spare Parts Ecosystem"),
        "what": ("Parts catalogue, cart, orders, payment and dealer stock.", "Katalog spare parts, keranjang, order, pembayaran, dan stok dealer."),
        "solves": ("Parts ordered by phone and spreadsheet, with no view of dealer stock.", "Order spare parts lewat telepon dan spreadsheet, tanpa gambaran stok dealer."),
        "features": [
            F(("Catalogue with categories", "Katalog dengan kategori"),
              ("Parts sit in nested categories, with images, SKU and compatible models.", "Spare parts tersusun dalam kategori bertingkat, dengan gambar, SKU, dan model yang kompatibel."),
              ("Dealers ordering the wrong part for a model.", "Dealer memesan part yang salah untuk sebuah model.")),
            F(("Cart and order lifecycle", "Keranjang dan siklus order"),
              ("A saved cart, then pending, approved, in preparation, delivered, paid and complete, linked to the SAP sales order.", "Keranjang yang tersimpan, lalu pending, approved, in preparation, delivered, paid, dan complete, terhubung ke sales order SAP."),
              ("Orders that exist in one system but not the other.", "Order yang ada di satu sistem tapi tidak ada di sistem lain.")),
            F(("Dealer-specific prices", "Harga khusus dealer"),
              ("Multi-level price tiers with special prices per dealer.", "Tier harga bertingkat dengan harga khusus per dealer."),
              ("Checking prices by hand on every order.", "Cek harga manual di setiap order.")),
            F(("Dealer stock and alerts", "Stok dealer dan alert"),
              ("Minimum stock levels, low-stock alerts and a stock movement history for dealers.", "Batas minimum stok, alert stok menipis, dan riwayat mutasi stok untuk dealer."),
              ("Dealers running out of fast-moving parts.", "Dealer kehabisan part yang cepat laku.")),
        ],
        "links": ["part_claims", "unit_master", "billing"],
    },
    {
        "id": "ppic", "no": 12, "cluster": "internal",
        "name": ("Manufacturing / PPIC", "Manufacturing / PPIC"),
        "what": ("Production plans, shifts, manpower parameters and holiday calendars.", "Rencana produksi, shift, parameter manpower, dan kalender libur."),
        "solves": ("Production plans kept in separate spreadsheets that the floor never sees.", "Rencana produksi di spreadsheet terpisah yang tidak pernah dilihat lantai produksi."),
        "features": [
            F(("Production PO and plan", "PO produksi dan plan"),
              ("Sales orders become production POs and plan items with target dates.", "Sales order menjadi PO produksi dan item plan dengan target tanggal."),
              ("Losing the link between what was sold and what gets built.", "Hilangnya hubungan antara yang dijual dan yang diproduksi.")),
            F(("Shift, process and manpower parameters", "Parameter shift, proses, dan manpower"),
              ("Shifts and breaks, the process sequence and manpower by position.", "Shift dan jam istirahat, urutan proses, serta manpower per posisi."),
              ("Targets that ignore breaks and actual staffing.", "Target yang tidak memperhitungkan istirahat dan jumlah orang sebenarnya.")),
            F(("Holiday calendar", "Kalender libur"),
              ("National and company holidays feed into planning.", "Libur nasional dan libur perusahaan masuk ke perencanaan."),
              ("Plans scheduled on days the plant is closed.", "Plan yang dijadwalkan di hari pabrik tutup.")),
            F(("Control room monitoring", "Monitoring control room"),
              ("A live target-versus-actual view of production.", "Tampilan live target vs aktual produksi."),
              ("Seeing yesterday's problems today.", "Baru melihat masalah kemarin di hari ini.")),
        ],
        "links": ["mes", "elhp", "vin", "order"],
    },
    {
        "id": "workload", "no": 13, "cluster": "internal",
        "name": ("Workload / Project Management", "Workload / Project Management"),
        "what": ("Internal projects and tasks with assignees, labels, files and comments.", "Project dan task internal dengan assignee, label, file, dan komentar."),
        "solves": ("Cross-department work tracked in personal notes and chat groups.", "Pekerjaan lintas departemen yang dicatat di catatan pribadi dan grup chat."),
        "features": [
            F(("Projects and task status", "Project dan status task"),
              ("Projects have an owner and period; tasks move through backlog, ready, in progress, review and done.", "Project punya owner dan periode; task bergerak dari backlog, ready, in progress, review, sampai done."),
              ("Not knowing what stage a piece of work is at.", "Tidak tahu pekerjaan sedang di tahap apa.")),
            F(("Assignees, comments and files", "Assignee, komentar, dan file"),
              ("Several assignees, comment threads with mentions and file attachments on each task.", "Beberapa assignee, thread komentar dengan mention, dan attachment di setiap task."),
              ("Decisions scattered across chats and email.", "Keputusan yang tercecer di chat dan email.")),
            F(("Approved deletions", "Penghapusan dengan approval"),
              ("Deleting a task needs the project admin's approval.", "Menghapus task butuh approval admin project."),
              ("Work disappearing by accident.", "Pekerjaan hilang karena terhapus tanpa sengaja.")),
            F(("Task dependencies", "Dependency antar task"),
              ("A task can't start until the task it depends on is done.", "Task tidak bisa dimulai sebelum task yang menjadi syaratnya selesai."),
              ("Work starting before its inputs are ready.", "Pekerjaan dimulai sebelum input-nya siap."), spec=True),
        ],
        "links": ["mom"],
    },
    {
        "id": "mom", "no": 14, "cluster": "internal",
        "name": ("Meeting Minutes", "Meeting Minutes (MoM)"),
        "what": ("Minutes with attendees, notes per department and tracked action items.", "Notulen dengan peserta, catatan per departemen, dan action item yang dilacak."),
        "solves": ("Action items agreed in a meeting and forgotten a week later.", "Action item yang disepakati di meeting lalu terlupakan seminggu kemudian."),
        "features": [
            F(("Meetings and attendance", "Meeting dan kehadiran"),
              ("Title, time, place or link, category, departments, agenda and attendees, including outside guests.", "Judul, waktu, tempat atau link, kategori, departemen, agenda, dan peserta, termasuk tamu dari luar."),
              ("No record of who was there when something was decided.", "Tidak ada catatan siapa yang hadir saat keputusan diambil.")),
            F(("Action items with owners", "Action item dengan PIC"),
              ("Each action has a person in charge, due date, priority and status.", "Setiap action punya PIC, due date, prioritas, dan status."),
              ("Tasks with no clear owner.", "Task tanpa pemilik yang jelas.")),
            F(("Actions become projects", "Action jadi project"),
              ("An action item can be turned into a project in Workload Management.", "Action item bisa diubah menjadi project di Workload Management."),
              ("Big follow-ups that live only in the minutes.", "Tindak lanjut besar yang hanya tersimpan di notulen.")),
            F(("AI tidy-up of notes", "Merapikan notulen dengan AI"),
              ("AI turns rough notes into structured minutes and pulls out the action items.", "AI mengubah catatan kasar menjadi notulen terstruktur dan mengambil action item-nya."),
              ("Time spent rewriting notes after every meeting.", "Waktu yang habis untuk menulis ulang catatan setelah setiap meeting."), spec=True),
        ],
        "links": ["workload", "customers"],
    },
    {
        "id": "socialization", "no": 15, "cluster": "marketing",
        "name": ("Socialization & Training Events", "Socialization & Training Events"),
        "what": ("Dealer events and trainings with invitations and attendance replies.", "Event dan training dealer dengan undangan dan konfirmasi kehadiran."),
        "solves": ("Chasing attendance confirmations dealer by dealer on WhatsApp.", "Mengejar konfirmasi kehadiran dealer satu per satu lewat WhatsApp."),
        "features": [
            F(("Event setup and targeting", "Setup event dan target"),
              ("Event details and platform, sent to all dealers or selected ones.", "Detail event dan platform, dikirim ke semua dealer atau dealer tertentu."),
              ("Invitations going to the wrong dealers.", "Undangan terkirim ke dealer yang salah.")),
            F(("A reply link for each dealer", "Link konfirmasi per dealer"),
              ("Each dealer gets a link to confirm owner and admin attendance without logging in, and can change the answer later.", "Setiap dealer mendapat link untuk konfirmasi kehadiran owner dan admin tanpa login, dan bisa mengubah jawabannya belakangan."),
              ("Replies lost because a dealer had no account or forgot the password.", "Jawaban hilang karena dealer tidak punya akun atau lupa password.")),
            F(("Attendance dashboard", "Dashboard kehadiran"),
              ("Invited, responded, owners attending and admins attending in one view.", "Jumlah diundang, sudah merespons, owner hadir, dan admin hadir dalam satu tampilan."),
              ("Counting replies by hand before the event.", "Menghitung jawaban secara manual sebelum event.")),
        ],
        "links": ["gamification", "csat"],
    },
    {
        "id": "promotion", "no": 16, "cluster": "marketing",
        "name": ("Promotion Materials", "Promotion Materials"),
        "what": ("A catalogue of brochures, posters and digital content dealers can request.", "Katalog brosur, poster, dan konten digital yang bisa di-request dealer."),
        "solves": ("Material requests by message, with stock checked only after a promise was made.", "Request material lewat pesan, dengan stok yang baru dicek setelah dijanjikan."),
        "features": [
            F(("Catalogue with stock", "Katalog dengan stok"),
              ("Items with type, SKU, images, downloadable files and stock thresholds.", "Item dengan tipe, SKU, gambar, file download, dan batas stok."),
              ("Not knowing what materials exist or how many are left.", "Tidak tahu material apa saja yang ada dan sisa berapa.")),
            F(("Request cart", "Keranjang request"),
              ("Dealers add items to a cart and submit with a purpose and optional budget.", "Dealer menambahkan item ke keranjang lalu submit dengan tujuan dan budget opsional."),
              ("Vague requests that need several rounds of questions.", "Request yang tidak jelas sehingga butuh beberapa kali tanya-jawab.")),
            F(("Approval through to shipment", "Approval sampai pengiriman"),
              ("Submitted, reviewed, approved, processing, shipped with a tracking number, completed.", "Submitted, reviewed, approved, processing, shipped dengan nomor resi, completed."),
              ("Dealers not knowing whether their materials were sent.", "Dealer tidak tahu apakah material mereka sudah dikirim.")),
            F(("Stock rules", "Aturan stok"),
              ("Physical items can't be requested beyond stock; digital items have no limit.", "Item fisik tidak bisa di-request melebihi stok; item digital tanpa batas."),
              ("Promising materials that aren't there.", "Menjanjikan material yang tidak tersedia.")),
        ],
        "links": ["content", "gamification"],
    },
    {
        "id": "gamification", "no": 17, "cluster": "marketing",
        "name": ("Gamification & Rewards", "Gamification & Rewards"),
        "what": ("Loyalty points for dealer actions, with a reward catalogue.", "Poin loyalitas untuk aktivitas dealer, dengan katalog reward."),
        "solves": ("Dealer incentive programmes tracked by hand with no running balance.", "Program insentif dealer yang dicatat manual tanpa saldo berjalan."),
        "features": [
            F(("Point rules", "Aturan poin"),
              ("Points are earned on set triggers, such as an order being completed.", "Poin didapat dari pemicu tertentu, misalnya order yang complete."),
              ("Different rewards for the same effort.", "Reward yang berbeda untuk usaha yang sama.")),
            F(("Point ledger", "Ledger poin"),
              ("Earn, burn, adjust and expire transactions, with a balance per dealer.", "Transaksi earn, burn, adjust, dan expire, dengan saldo per dealer."),
              ("Arguments about how many points a dealer has.", "Perdebatan soal jumlah poin yang dimiliki dealer.")),
            F(("Reward catalogue and redemption", "Katalog reward dan redemption"),
              ("Rewards have a point cost and stock; redemptions go from requested to approved to fulfilled.", "Reward punya harga poin dan stok; redemption bergerak dari requested ke approved sampai fulfilled."),
              ("Redemptions handled informally.", "Penukaran reward yang ditangani secara informal.")),
            F(("Ranking and levels", "Ranking dan level"),
              ("Dealer ranking, badges and levels on a performance dashboard.", "Ranking dealer, badge, dan level di dashboard performa."),
              ("No visible reason for dealers to do more.", "Tidak ada alasan yang terlihat bagi dealer untuk berbuat lebih.")),
        ],
        "links": ["order", "socialization", "csat"],
    },
    {
        "id": "content", "no": 18, "cluster": "marketing",
        "name": ("Marketing Content Distribution", "Marketing Content Distribution"),
        "what": ("Digital content sent to dealer segments, with their social accounts and engagement.", "Konten digital yang dikirim ke segmen dealer, beserta akun sosmed dan engagement-nya."),
        "solves": ("Content shared in chat groups with no idea whether dealers posted it.", "Konten yang dibagikan di grup chat tanpa tahu apakah dealer mem-posting-nya."),
        "features": [
            F(("Content library", "Library konten"),
              ("Photos, videos and audio kept in one asset library.", "Foto, video, dan audio tersimpan dalam satu library aset."),
              ("Dealers using old or off-brand material.", "Dealer memakai material lama atau yang tidak sesuai brand.")),
            F(("Distribution to dealer segments", "Distribusi ke segmen dealer"),
              ("Content goes to a segment or to chosen dealers.", "Konten dikirim ke segmen atau dealer yang dipilih."),
              ("The same content for very different areas.", "Konten yang sama untuk wilayah yang sangat berbeda.")),
            F(("Dealer social accounts and engagement", "Akun sosmed dealer dan engagement"),
              ("Dealers register Instagram, Facebook or TikTok accounts; likes, shares, comments and reach are recorded per post.", "Dealer mendaftarkan akun Instagram, Facebook, atau TikTok; like, share, komentar, dan reach dicatat per posting."),
              ("No way to compare which content worked.", "Tidak ada cara membandingkan konten mana yang berhasil.")),
        ],
        "links": ["promotion", "csat"],
    },
    {
        "id": "csat", "no": 19, "cluster": "marketing",
        "name": ("CSAT Survey", "CSAT Survey"),
        "what": ("Satisfaction surveys, customer journey stages and dealer levels.", "Survei kepuasan, tahapan customer journey, dan level dealer."),
        "solves": ("Satisfaction measured rarely and kept apart from dealer data.", "Kepuasan yang jarang diukur dan disimpan terpisah dari data dealer."),
        "features": [
            F(("Survey projects and form builder", "Project survei dan form builder"),
              ("Survey projects per period and segment, with ratings, multiple choice and open text.", "Project survei per periode dan segmen, dengan rating, pilihan ganda, dan teks bebas."),
              ("One-off surveys that can't be compared over time.", "Survei sekali jalan yang tidak bisa dibandingkan dari waktu ke waktu.")),
            F(("Journey stages", "Tahapan journey"),
              ("Awareness, consideration, purchase, service and loyalty stages, traced per dealer.", "Tahap awareness, consideration, purchase, service, dan loyalty, ditelusuri per dealer."),
              ("Not knowing where in the journey customers drop off.", "Tidak tahu di tahap journey mana customer berhenti.")),
            F(("Dealer levels from scores", "Level dealer dari skor"),
              ("Platinum, gold, silver and bronze levels set by rules on survey scores.", "Level platinum, gold, silver, dan bronze ditentukan aturan berdasarkan skor survei."),
              ("Dealer rankings based on opinion instead of scores.", "Ranking dealer yang berdasarkan opini, bukan skor.")),
        ],
        "links": ["customers", "gamification"],
    },
    {
        "id": "rbac", "no": 20, "cluster": "platform",
        "name": ("Users, Roles & Permissions", "Users, Roles & Permissions"),
        "what": ("Who can see and do what, down to the dealers a sales area manager covers.", "Siapa bisa melihat dan melakukan apa, sampai dealer yang di-cover seorang sales area manager."),
        "solves": ("Shared logins, and dealers able to see each other's data.", "Login yang dipakai bersama, dan dealer yang bisa melihat data dealer lain."),
        "features": [
            F(("Roles and permission table", "Role dan tabel permission"),
              ("Eight core roles plus custom ones, set through a permission table.", "Delapan role inti plus role custom, diatur lewat tabel permission."),
              ("Access decided case by case.", "Akses yang ditentukan kasus per kasus.")),
            F(("Dealer isolation and SAM coverage", "Isolasi dealer dan cakupan SAM"),
              ("Dealers see only their own data; a sales area manager sees only assigned dealers.", "Dealer hanya melihat datanya sendiri; sales area manager hanya melihat dealer yang ditugaskan."),
              ("Data leaking between competing dealers.", "Data yang bocor antar dealer yang saling bersaing.")),
            F(("Onboarding and passwords", "Onboarding dan password"),
              ("Bulk user import, a forced password change on first login and password reset.", "Bulk import user, wajib ganti password saat login pertama, dan reset password."),
              ("Weak default passwords left in place.", "Password default yang lemah dibiarkan.")),
            F(("Role switching for testing", "Role switching untuk testing"),
              ("An admin can act as another role to test without logging out.", "Admin bisa bertindak sebagai role lain untuk testing tanpa logout."),
              ("Testing permissions by borrowing someone's account.", "Mengetes permission dengan meminjam akun orang lain.")),
        ],
        "links": ["platform", "order", "customers"],
    },
    {
        "id": "platform", "no": 21, "cluster": "platform",
        "name": ("Platform Services", "Platform Services"),
        "what": ("Notifications, logs, bug reports, maintenance windows and two languages for every module.", "Notifikasi, log, bug report, jadwal maintenance, dan dua bahasa untuk setiap modul."),
        "solves": ("Each module handling alerts, logs and support in its own way.", "Setiap modul menangani notifikasi, log, dan support dengan caranya sendiri."),
        "features": [
            F(("In-app notifications", "Notifikasi in-app"),
              ("A notification centre with unread badges and preferences per user.", "Notification center dengan badge unread dan preferensi per user."),
              ("People hearing about changes late, or only through chat.", "Orang baru tahu perubahan terlambat, atau hanya lewat chat.")),
            F(("Activity and audit logs", "Activity log dan audit log"),
              ("Changes to key records are logged with old and new values, and audit entries can't be edited.", "Perubahan pada data penting dicatat dengan nilai lama dan baru, dan entri audit tidak bisa diubah."),
              ("No reliable answer to what changed and who did it.", "Tidak ada jawaban yang bisa dipercaya soal apa yang berubah dan siapa pelakunya.")),
            F(("Bug reports and feedback", "Bug report dan feedback"),
              ("Users report issues with a severity and screenshots, and each report is tracked to resolved or closed.", "User melaporkan masalah dengan tingkat severity dan screenshot, dan setiap laporan dilacak sampai resolved atau closed."),
              ("Problems reported by phone and never followed up.", "Masalah yang dilaporkan lewat telepon dan tidak pernah ditindaklanjuti.")),
            F(("Two languages and region data", "Dua bahasa dan data wilayah"),
              ("Indonesian and English interface, plus province-to-village region data for address forms.", "Tampilan Bahasa Indonesia dan English, plus data wilayah provinsi sampai kelurahan untuk form alamat."),
              ("Staff and dealers working in different languages, and inconsistent addresses.", "Staf dan dealer yang bekerja dengan bahasa berbeda, serta alamat yang tidak konsisten.")),
            F(("Session control and maintenance windows", "Kontrol session dan jadwal maintenance"),
              ("Admins see active sessions and failed logins, can force a logout, and schedule maintenance with a banner.", "Admin bisa melihat session aktif dan login gagal, memaksa logout, dan menjadwalkan maintenance dengan banner."),
              ("Surprise downtime and suspicious logins going unnoticed.", "Downtime mendadak dan login mencurigakan yang tidak terdeteksi.")),
        ],
        "links": ["rbac", "customers"],
    },
    {
        "id": "mes", "no": 22, "cluster": "floor",
        "name": ("Production Kiosk & MES", "Production Kiosk & MES"),
        "what": ("QR kiosks at each post that record units, output and cycle time.", "Kiosk QR di setiap pos yang mencatat unit, output, dan cycle time."),
        "solves": ("Stamped numbers and output counted on paper and checked a day later.", "Nomor yang diketok dan output yang dihitung di kertas, lalu baru dicek sehari kemudian."),
        "features": [
            F(("QR registry per unit", "Registry QR per unit"),
              ("Each unit has a stable QR code that is scanned at every post.", "Setiap unit punya kode QR tetap yang di-scan di setiap pos."),
              ("Typing the same unit number again at every station.", "Mengetik ulang nomor unit yang sama di setiap stasiun.")),
            F(("Kiosk modes", "Mode kiosk"),
              ("Light sign-in, plus buffer and guest modes, keep the floor working.", "Login ringan, plus mode buffer dan guest, supaya lantai produksi tetap jalan."),
              ("Production stopping because someone can't log in.", "Produksi berhenti karena seseorang tidak bisa login.")),
            F(("Output recap by group", "Rekap output per grup"),
              ("Output is counted per group, such as full assembly and CKD.", "Output dihitung per grup, misalnya full assembly dan CKD."),
              ("End-of-shift tallies done by hand.", "Hitungan akhir shift yang dikerjakan manual.")),
            F(("Cycle time with deviation flags", "Cycle time dengan flag deviasi"),
              ("Cycle time is compared with PPIC parameters on the server clock, and deviations are flagged.", "Cycle time dibandingkan dengan parameter PPIC memakai jam server, dan deviasinya ditandai."),
              ("Slow posts noticed only in the daily report, and times changed on local devices.", "Pos yang lambat baru terlihat di laporan harian, dan jam yang diubah di perangkat lokal.")),
        ],
        "links": ["ppic", "vin", "elhp", "internal_qc"],
    },
    {
        "id": "elhp", "no": 23, "cluster": "floor",
        "name": ("E-LHP & Finished Goods", "E-LHP & Finished Goods"),
        "what": ("The daily production report and the chain from stock to delivery.", "Laporan hasil produksi harian dan rantai dari stok sampai delivery."),
        "solves": ("Daily production reports put together by hand from several sources.", "Laporan produksi harian yang disusun manual dari beberapa sumber."),
        "features": [
            F(("Printable daily E-LHP", "E-LHP harian siap cetak"),
              ("The daily report is built from PPIC parameters and kiosk output, and becomes final once the day's data is locked.", "Laporan harian disusun dari parameter PPIC dan output kiosk, dan menjadi final setelah data hari itu dikunci."),
              ("Reports changing after they were signed.", "Laporan yang berubah setelah ditandatangani.")),
            F(("Finished-goods stock", "Stok barang jadi"),
              ("Stock levels come from registered chassis and engine numbers.", "Level stok berasal dari nomor rangka dan mesin yang sudah teregistrasi."),
              ("Stock counts that don't match what was built.", "Hitungan stok yang tidak cocok dengan yang diproduksi.")),
            F(("From PDI to the delivery report", "Dari PDI sampai delivery report"),
              ("Units pass PDI, then show up on the delivery report and the finished-goods dashboard.", "Unit melewati PDI, lalu muncul di delivery report dan dashboard barang jadi."),
              ("Losing sight of units between the line and the truck.", "Kehilangan jejak unit di antara lini produksi dan truk.")),
        ],
        "links": ["mes", "ppic", "delivery_prep", "qi"],
    },
    {
        "id": "internal_qc", "no": 24, "cluster": "floor",
        "name": ("Internal QC (in-process)", "Internal QC (in-process)"),
        "what": ("Quality checks and repairs on the production line, separate from pre-delivery inspection.", "Pengecekan kualitas dan repair di lini produksi, terpisah dari inspeksi pra-pengiriman."),
        "solves": ("NG units moving to the next stage before they were fixed.", "Unit NG yang lanjut ke tahap berikutnya sebelum diperbaiki."),
        "features": [
            F(("In-process inspection", "Inspeksi in-process"),
              ("Checklist items and a status per part, linked to the unit being built.", "Item checklist dan status per komponen, terhubung ke unit yang sedang diproduksi."),
              ("Defects found only at final inspection.", "Cacat yang baru ditemukan saat inspeksi akhir.")),
            F(("NG and repair tracking", "Tracking NG dan repair"),
              ("NG parts and the repair done on them, with a repair status.", "Komponen NG dan repair yang dikerjakan, lengkap dengan status repair."),
              ("Not knowing whether a repair was actually done.", "Tidak tahu apakah repair benar-benar sudah dikerjakan.")),
            F(("Hold until repaired", "Tahan sampai diperbaiki"),
              ("A unit with a critical NG can't move on until the repair is verified.", "Unit dengan NG kritis tidak bisa lanjut sebelum repair-nya terverifikasi."),
              ("Critical defects slipping through to delivery.", "Cacat kritis yang lolos sampai delivery.")),
            F(("NG trends", "Tren NG"),
              ("NG trends are reported for continuous improvement.", "Tren NG dilaporkan untuk continuous improvement."),
              ("Fixing the same defect again and again.", "Memperbaiki cacat yang sama berulang kali.")),
        ],
        "links": ["mes", "qi", "ksg"],
    },
    {
        "id": "customers", "no": 25, "cluster": "floor",
        "name": ("Customer Database & Bottleneck View", "Customer Database & Bottleneck View"),
        "what": ("One customer record reused across modules, and a view of where work is stuck.", "Satu data customer yang dipakai ulang lintas modul, dan tampilan di mana pekerjaan tertahan."),
        "solves": ("Customer details typed again for every document, and delays found only when someone complains.", "Data customer yang diketik ulang untuk setiap dokumen, dan keterlambatan yang baru ketahuan saat ada yang komplain."),
        "features": [
            F(("Customer master", "Master customer"),
              ("Identity, a region-resolved address and tax or ID numbers, reused in legal requests and inspections without duplicates.", "Identitas, alamat yang ter-resolve ke wilayah, serta NPWP atau NIK, dipakai ulang di legal request dan inspeksi tanpa duplikasi."),
              ("The same buyer stored three times with three spellings.", "Pembeli yang sama tersimpan tiga kali dengan tiga ejaan.")),
            F(("Bottleneck view across processes", "Tampilan bottleneck lintas proses"),
              ("Shows ageing items from about 14 process sources, such as orders, legal requests, inspections, claims and meeting actions.", "Menampilkan item yang menua dari sekitar 14 sumber proses, seperti order, legal request, inspeksi, klaim, dan action meeting."),
              ("Delays hidden inside individual modules.", "Keterlambatan yang tersembunyi di dalam modul masing-masing.")),
            F(("Who is holding it", "Siapa yang menahan"),
              ("Names the person or role responsible at each stuck step, with age buckets you can set.", "Menunjukkan orang atau role yang bertanggung jawab di setiap tahap yang tertahan, dengan age bucket yang bisa diatur."),
              ("Follow-ups that chase everyone instead of the one person who can act.", "Follow-up yang mengejar semua orang, bukan satu orang yang bisa bertindak.")),
        ],
        "links": ["legal", "qi", "csat", "rbac"],
    },
]

JOURNEY = [
    ("unit_master", ("Unit master", "Unit master")),
    ("order", ("Dealer order", "Order dealer")),
    ("ppic", ("Production plan", "Rencana produksi")),
    ("mes", ("Kiosk scan", "Scan kiosk")),
    ("vin", ("Chassis & engine numbers", "Nomor rangka & mesin")),
    ("internal_qc", ("In-process QC", "QC in-process")),
    ("elhp", ("Daily report & stock", "Laporan harian & stok")),
    ("qi", ("Pre-delivery inspection", "Inspeksi pra-pengiriman")),
    ("delivery_prep", ("Delivery prep", "Persiapan delivery")),
    ("billing", ("Payment", "Pembayaran")),
    ("legal", ("Registration papers", "Dokumen registrasi")),
    ("ksg", ("Warranty claims", "Klaim garansi")),
]

UNDERLAY = [
    ("rbac", ("Roles & permissions", "Role & permission")),
    ("platform", ("Notifications & audit log", "Notifikasi & audit log")),
    ("customers", ("Customer data & bottleneck view", "Data customer & tampilan bottleneck")),
]

LANES = [
    (("Spare parts", "Spare parts"), ("Its own catalogue, orders and claims.", "Katalog, order, dan klaimnya sendiri."), ["parts", "part_claims"]),
    (("Dealer marketing", "Marketing dealer"), ("Keeps dealers active between orders.", "Menjaga dealer tetap aktif di antara order."), ["socialization", "promotion", "gamification", "content", "csat"]),
    (("Internal work", "Kerja internal"), ("The meetings and projects behind the changes.", "Meeting dan project di balik setiap perubahan."), ["mom", "workload"]),
]

RULES = [
    (("Finishing a pre-delivery inspection moves the order to received.", "Inspeksi pra-pengiriman yang selesai memindahkan order ke status received."), ["qi", "order"]),
    (("Every NG part found in inspection becomes a delivery claim candidate once the unit is delivered.", "Setiap komponen NG dari inspeksi menjadi kandidat delivery claim setelah unit dikirim."), ["qi", "delivery_claims"]),
    (("An order can't be marked delivered until delivery prep is complete and inspection is done.", "Order tidak bisa ditandai delivered sebelum persiapan delivery lengkap dan inspeksi selesai."), ["delivery_prep", "qi", "order"]),
    (("An order can't be billed without a confirmed payment proof.", "Order tidak bisa di-bill tanpa bukti bayar yang sudah dikonfirmasi."), ["billing", "order"]),
    (("Each registration request belongs to one chassis number, and the BBN faktur prints only after the order is complete.", "Setiap pengajuan registrasi terikat ke satu nomor rangka, dan BBN faktur baru bisa dicetak setelah order complete."), ["legal", "vin", "order"]),
    (("An approved warranty replacement creates a linked replacement order.", "Replacement garansi yang di-approve membuat order pengganti yang terhubung."), ["ksg", "order"]),
    (("Kiosk output and PPIC parameters build the daily production report.", "Output kiosk dan parameter PPIC menyusun laporan produksi harian."), ["mes", "ppic", "elhp"]),
    (("A unit with a critical NG in in-process QC can't move on until the repair is verified.", "Unit dengan NG kritis di QC in-process tidak bisa lanjut sebelum repair-nya terverifikasi."), ["internal_qc", "mes"]),
    (("A meeting action item can become a project.", "Action item dari meeting bisa menjadi project."), ["mom", "workload"]),
    (("A sales area manager only sees the dealers assigned to them, in every module.", "Sales area manager hanya melihat dealer yang ditugaskan kepadanya, di semua modul."), ["rbac"]),
]

USERS = [
    (("Manufacturing", "Manufaktur"), ("Production, quality, PPIC and logistics.", "Produksi, quality, PPIC, dan logistik."), ["ppic", "mes", "internal_qc", "elhp", "vin"]),
    (("Sales & marketing", "Sales & marketing"), ("Sales admins, sales area managers and marketing.", "Sales admin, sales area manager, dan marketing."), ["order", "legal", "promotion", "csat"]),
    (("Administration", "Administrasi"), ("Finance, legal and system admins.", "Finance, legal, dan system admin."), ["billing", "rbac", "platform"]),
    (("Dealers", "Dealer"), ("Owners, admins and operators across Indonesia.", "Owner, admin, dan operator di seluruh Indonesia."), ["order", "delivery_claims", "ksg", "parts"]),
]


def build(b):
    lang = b.LANG
    E = b.E

    def L(pair):
        return pair[0] if lang == "en" else pair[1]

    def LE(pair):
        return E(L(pair))

    mod = {m["id"]: m for m in MODULES}

    def chip(mid, label=None):
        text = L(label) if label else L(mod[mid]["name"])
        return f'<a class="ps-chip" href="#m-{mid}" data-open-module="{mid}">{E(text)}</a>'

    stats = [
        ("25", ("modules", "modul")),
        ("6", ("module groups", "kelompok modul")),
        ("8", ("core user roles", "role user inti")),
        ("EN · ID", ("interface languages", "bahasa tampilan")),
    ]
    stats_html = "".join(f"<div><dt>{LE(lbl)}</dt><dd>{E(v)}</dd></div>" for v, lbl in stats)
    proof = [
        (("1,043", "1.043"), ("commits, Oct 2025 – Sep 2026", "commit, Okt 2025 – Sep 2026")),
        (("15/22", "15/22"), ("dealers active, May–Jun 2026", "dealer aktif, Mei–Jun 2026")),
        (("4,818", "4.818"), ("unit records by Sep 2026", "data unit per Sep 2026")),
    ]
    proof_html = "".join(f"<div><b>{LE(v)}</b><small>{LE(lbl)}</small></div>" for v, lbl in proof)

    hero = f"""
<div class="wrap ps-page">
  <p class="crumbs"><a href="index.html#work">{LE(("Work", "Project"))}</a> / PowerSync</p>
  <section class="ps-hero paper" aria-labelledby="ps-title">
    <div class="ps-hero-copy">
      <span class="eyebrow"><span class="tiny-line"></span> PowerSync · Feature explorer</span>
      <h1 id="ps-title">{L(("One platform for the whole<br><span>life of a vehicle.</span>", "Satu platform untuk seluruh<br><span>perjalanan kendaraan.</span>"))}</h1>
      <p class="lede">{LE(("PowerSync is the web platform I led at PT Dharma Polimetal. It connects dealer orders, production, quality checks, delivery, registration paperwork, claims and dealer marketing, so one unit can be followed from order to customer.", "PowerSync adalah platform web yang saya pimpin di PT Dharma Polimetal. Platform ini menyambungkan order dealer, produksi, quality check, delivery, dokumen registrasi, klaim, dan marketing dealer, sehingga satu unit bisa ditelusuri dari order sampai ke customer."))}</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="#modules">{LE(("Explore the modules", "Jelajahi modulnya"))} <span aria-hidden="true">↓</span></a>
        <a class="text-link" href="work-powersync-dealer.html">{LE(("Read the case study", "Baca case study"))} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <div class="ps-hero-side">
      <dl class="ps-stats">{stats_html}</dl>
      <div class="ps-proof">{proof_html}</div>
    </div>
  </section>"""

    journey_items = "".join(
        f'<li><a class="ps-node" href="#m-{mid}" data-open-module="{mid}"><small>{mod[mid]["no"]:02d}</small><span>{LE(label)}</span></a></li>'
        for mid, label in JOURNEY
    )
    underlay = "".join(chip(mid, label) for mid, label in UNDERLAY)
    lanes = "".join(
        f'<article class="ps-lane paper"><h3>{LE(title)}</h3><p>{LE(desc)}</p><div class="ps-chips">{"".join(chip(m) for m in mids)}</div></article>'
        for title, desc, mids in LANES
    )
    connect = f"""
  <section class="section" id="connect" aria-labelledby="connect-h">
    <div class="section-head">
      <span class="eyebrow">01 / {LE(("How it connects", "Cara modulnya terhubung"))}</span>
      <h2 id="connect-h">{LE(("Follow one unit through the system", "Ikuti satu unit di dalam sistem"))}</h2>
      <p>{LE(("Each step below is a module. Select one to open its features.", "Setiap langkah di bawah adalah satu modul. Pilih salah satu untuk membuka fiturnya."))}</p>
    </div>
    <div class="ps-map paper">
      <ol class="ps-journey">{journey_items}</ol>
      <div class="ps-underlay"><span class="mono">{LE(("Running under every step", "Berjalan di bawah setiap langkah"))}</span><div class="ps-chips">{underlay}</div></div>
    </div>
    <div class="ps-lanes">{lanes}</div>
  </section>"""

    rules = "".join(
        f'<li><p>{LE(text)}</p><div class="ps-chips">{"".join(chip(m) for m in mids)}</div></li>'
        for text, mids in RULES
    )
    rules_section = f"""
  <section class="section" id="rules" aria-labelledby="rules-h">
    <div class="section-head">
      <span class="eyebrow">02 / {LE(("Rules between modules", "Aturan antar modul"))}</span>
      <h2 id="rules-h">{LE(("What one module changes in another", "Apa yang diubah satu modul di modul lain"))}</h2>
      <p>{LE(("From the requirements spec. Each rule keeps a step from happening out of order.", "Diambil dari requirement spec. Setiap aturan mencegah sebuah langkah terjadi tidak berurutan."))}</p>
    </div>
    <ol class="ps-rules">{rules}</ol>
  </section>"""

    feature_word = ("features", "fitur")
    module_word = ("modules", "modul")

    def module_html(m):
        features = []
        for f in m["features"]:
            spec = f' <span class="chip chip--spec">{LE(SPEC)}</span>' if f["spec"] else ""
            features.append(
                f'<li><details class="ps-feature"><summary><span>{LE(f["name"])}</span>{spec}</summary>'
                f'<div class="ps-feature-body"><div><span class="mono">{LE(("What it does", "Fungsinya"))}</span><p>{LE(f["does"])}</p></div>'
                f'<div><span class="mono">{LE(("What it solves", "Yang diselesaikan"))}</span><p>{LE(f["solves"])}</p></div></div></details></li>'
            )
        links = "".join(chip(x) for x in m["links"])
        return f"""
      <details class="ps-module paper" id="m-{m['id']}" data-cluster="{m['cluster']}">
        <summary><span class="ps-no">{m['no']:02d}</span><span class="ps-sum"><strong>{LE(m['name'])}</strong><small>{LE(m['what'])}</small></span><span class="ps-meta">{len(m['features'])} {LE(feature_word)}</span><span class="ps-chevron" aria-hidden="true"></span></summary>
        <div class="ps-body">
          <div class="ps-solves"><span class="mono">{LE(("The problem it solves", "Masalah yang diselesaikan"))}</span><p>{LE(m['solves'])}</p></div>
          <div><p class="mono ps-label">{LE(("Features", "Fitur"))}</p><ul class="ps-features">{''.join(features)}</ul></div>
          <div class="ps-links"><span class="mono">{LE(("Connected modules", "Modul terhubung"))}</span><div class="ps-chips">{links}</div></div>
        </div>
      </details>"""

    clusters = []
    for c in CLUSTERS:
        mods = [m for m in MODULES if m["cluster"] == c["id"]]
        clusters.append(f"""
    <div class="ps-cluster" data-cluster-group="{c['id']}">
      <header class="ps-cluster-head"><span class="ps-letter" aria-hidden="true">{c['letter']}</span><div><h3>{LE(c['name'])}</h3><p>{LE(c['desc'])}</p></div><span class="ps-count">{len(mods)} {LE(module_word)}</span></header>
      <div class="ps-modules">{''.join(module_html(m) for m in mods)}</div>
    </div>""")

    filter_buttons = f'<button type="button" data-cluster-filter="all" aria-pressed="true">{LE(("All", "Semua"))}</button>' + "".join(
        f'<button type="button" data-cluster-filter="{c["id"]}" aria-pressed="false"><b>{c["letter"]}</b>{LE(c["name"])}</button>' for c in CLUSTERS
    )
    explorer = f"""
  <section class="section" id="modules" aria-labelledby="modules-h" data-ps-explorer>
    <div class="section-head">
      <span class="eyebrow">03 / {LE(("All modules", "Semua modul"))}</span>
      <h2 id="modules-h">{LE(("Open a module to see its features", "Buka modul untuk melihat fiturnya"))}</h2>
      <p>{LE(("Each feature says what it does and the problem it solves.", "Setiap fitur menjelaskan fungsinya dan masalah yang diselesaikannya."))}</p>
    </div>
    <div class="ps-toolbar">
      <div class="ps-filter" role="group" aria-label="{LE(("Filter by module group", "Filter per kelompok modul"))}">{filter_buttons}</div>
      <label class="ps-search" for="ps-search"><span class="sr-only">{LE(("Search modules and features", "Cari modul dan fitur"))}</span><input type="search" id="ps-search" placeholder="{LE(("Search, e.g. faktur or QR", "Cari, misalnya faktur atau QR"))}" autocomplete="off"></label>
      <button type="button" class="btn ps-toggle" data-expand-all aria-pressed="false" data-label-expand="{LE(("Expand all", "Buka semua"))}" data-label-collapse="{LE(("Collapse all", "Tutup semua"))}">{LE(("Expand all", "Buka semua"))}</button>
    </div>
    <p class="ps-status" data-ps-status data-many="{LE(("{n} modules shown.", "{n} modul ditampilkan."))}" aria-live="polite"></p>
    {''.join(clusters)}
    <p class="ps-empty paper" data-ps-empty hidden>{LE(("No module matches that search.", "Tidak ada modul yang cocok dengan pencarian itu."))}</p>
  </section>"""

    users = "".join(
        f'<article class="ps-user paper"><h3>{LE(name)}</h3><p>{LE(desc)}</p><div class="ps-chips">{"".join(chip(m) for m in mids)}</div></article>'
        for name, desc, mids in USERS
    )
    users_section = f"""
  <section class="section" id="users" aria-labelledby="users-h">
    <div class="section-head">
      <span class="eyebrow">04 / {LE(("Who uses it", "Siapa yang memakai"))}</span>
      <h2 id="users-h">{LE(("Who works in PowerSync", "Siapa yang bekerja di PowerSync"))}</h2>
    </div>
    <div class="ps-users">{users}</div>
  </section>
  <section class="section ps-note" aria-labelledby="note-h">
    <div class="paper ps-note-card">
      <span class="mono" id="note-h">{LE(("About this page", "Tentang halaman ini"))}</span>
      <p>{LE(("The module and feature map follows the PowerSync requirements spec (July 2026). Every module has routes in the live codebase. Features tagged as spec items are optional parts of the spec that I haven't confirmed in the build. System figures come from the verified evidence behind my case studies.", "Peta modul dan fitur ini mengikuti requirement spec PowerSync (Juli 2026). Setiap modul punya route di codebase yang berjalan. Fitur yang ditandai sebagai item spec adalah bagian opsional dari spec yang belum saya konfirmasi di build. Angka sistem berasal dari bukti terverifikasi di balik case study saya."))}</p>
      <div class="btn-row">
        <a class="btn" href="work-powersync-dealer.html">{LE(("Case study: dealer platform", "Case study: platform dealer"))} <span aria-hidden="true">↗</span></a>
        <a class="btn" href="work-powersync-mes.html">{LE(("Case study: manufacturing & traceability", "Case study: manufacturing & traceability"))} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </section>
</div>"""

    title = L(("PowerSync feature explorer", "PowerSync feature explorer")) + " · Reyza Agung Gunawan"
    description = L((
        "Explore PowerSync's 25 connected modules, from dealer orders and production kiosks to registration papers and warranty claims, and the problem each feature solves.",
        "Jelajahi 25 modul PowerSync yang saling terhubung, dari order dealer dan kiosk produksi sampai dokumen registrasi dan klaim garansi, beserta masalah yang diselesaikan setiap fitur.",
    ))
    b.page("powersync.html", title, description, hero + connect + rules_section + explorer + users_section, active="powersync", body_class="theme-red")
