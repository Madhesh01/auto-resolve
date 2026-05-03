CREATE TABLE IF NOT EXISTS orders (
    order_no INTEGER PRIMARY KEY,
    address  VARCHAR NOT NULL,
    status   VARCHAR NOT NULL,
    price    NUMERIC NOT NULL
);

INSERT INTO orders (order_no, address, status, price) VALUES
    (1001, '12 MG Road, Bengaluru, KA 560001, India',              'PLACED',            1299),
    (1002, '45 Anna Salai, Chennai, TN 600002, India',              'CONFIRMED',          499),
    (1003, '78 Jubilee Hills, Hyderabad, TS 500033, India',         'SHIPPED',           2499),
    (1004, '22 Park Street, Kolkata, WB 700016, India',             'OUT_FOR_DELIVERY',   799),
    (1005, '9 Connaught Place, New Delhi, DL 110001, India',        'DELIVERED',         3999),
    (1006, '14 Banjara Hills, Hyderabad, TS 500034, India',         'PLACED',             149),
    (1007, '5 Brigade Road, Bengaluru, KA 560025, India',           'CONFIRMED',          999),
    (1008, '33 Marine Drive, Mumbai, MH 400020, India',             'PLACED',            5499),
    (1009, '101 Andheri West, Mumbai, MH 400053, India',            'PLACED',             299),
    (1010, '56 Sector 18, Noida, UP 201301, India',                 'PLACED',            1799),
    (1011, '88 FC Road, Pune, MH 411004, India',                    'SHIPPED',            649),
    (1012, '17 CG Road, Ahmedabad, GJ 380006, India',               'DELIVERED',         2199),
    (1013, '3 MI Road, Jaipur, RJ 302001, India',                   'PLACED',             399),
    (1014, '64 Hazratganj, Lucknow, UP 226001, India',              'CONFIRMED',         4299),
    (1015, '29 Ring Road, Surat, GJ 395002, India',                 'SHIPPED',            899),
    (1016, '11 Sector 17, Chandigarh, CH 160017, India',            'OUT_FOR_DELIVERY',  1599),
    (1017, '52 MP Nagar, Bhopal, MP 462011, India',                 'PLACED',             749),
    (1018, '7 Vijay Nagar, Indore, MP 452010, India',               'CONFIRMED',         3299),
    (1019, '19 Boring Road, Patna, BR 800001, India',               'PLACED',             199),
    (1020, '41 MG Road, Kochi, KL 682016, India',                   'SHIPPED',           2799),
    (1021, '6 Avinashi Road, Coimbatore, TN 641018, India',         'DELIVERED',         1099),
    (1022, '73 Beach Road, Visakhapatnam, AP 530001, India',        'PLACED',             549),
    (1023, '38 Wardha Road, Nagpur, MH 440010, India',              'CONFIRMED',         4799),
    (1024, '15 Alkapuri, Vadodara, GJ 390007, India',               'OUT_FOR_DELIVERY',  1349),
    (1025, '90 DLF Phase 1, Gurgaon, HR 122002, India',             'PLACED',            2099)
ON CONFLICT (order_no) DO NOTHING;
