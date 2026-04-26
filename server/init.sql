CREATE TABLE IF NOT EXISTS orders (
    order_no INTEGER PRIMARY KEY,
    address  VARCHAR NOT NULL,
    status   VARCHAR NOT NULL
);

INSERT INTO orders (order_no, address, status) VALUES
    (1001, '12 MG Road, Bengaluru, KA 560001, India',        'PLACED'),
    (1002, '45 Anna Salai, Chennai, TN 600002, India',        'CONFIRMED'),
    (1003, '78 Jubilee Hills, Hyderabad, TS 500033, India',   'SHIPPED'),
    (1004, '22 Park Street, Kolkata, WB 700016, India',       'OUT_FOR_DELIVERY'),
    (1005, '9 Connaught Place, New Delhi, DL 110001, India',  'DELIVERED'),
    (1006, '14 Banjara Hills, Hyderabad, TS 500034, India',   'PLACED'),
    (1007, '5 Brigade Road, Bengaluru, KA 560025, India',     'CONFIRMED'),
    (1008, '33 Marine Drive, Mumbai, MH 400020, India',       'PLACED'),
    (1009, '101 Andheri West, Mumbai, MH 400053, India',      'PLACED'),
    (1010, '56 Sector 18, Noida, UP 201301, India',           'PLACED')
ON CONFLICT (order_no) DO NOTHING;
