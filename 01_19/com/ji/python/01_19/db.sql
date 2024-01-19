CREATE TABLE place(
	p_info varchar2(50 char) PRIMARY KEY,
	p_x number(9,6) NOT NULL,
	p_y number(8,6) NOT NULL
)

DROP TABLE place

DROP SEQUENCE place_seq

SELECT * FROM place

SELECT NVL(null,'-'),NVL('NULL','-') FROM dual

SELECT NVL2(null,'A','B'),NVL2('NULL','A','B') FROM dual