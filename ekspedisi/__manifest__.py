{
    'name': 'ekspedisi',  #nama modul yg dibaca user di UI
    'version': '1.0.0',
    'author': 'Kevin',
    'summary': 'Modul ekspedisi', #deskripsi singkat dari modul
    'description': 'Modul ekspedisi', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [ #kalo update manifest jangan lupa update app list
        'security/ir.model.access.csv',
        'views/customer_view.xml',
        'views/gudang_view.xml',
        'views/jenisbarang_view.xml',
        'views/karyawan_view.xml',
        'views/kendaraan_view.xml',
        'views/pemesanan_view.xml',
        'views/pengambilan_view.xml',
        'views/vendor_view.xml',
        'wizard/wiz_ekspedisi_pemesanan_view.xml'
    ],
    'qweb': [],  #untuk memberi tahu static file, misal CSS
    'demo': [],  #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}