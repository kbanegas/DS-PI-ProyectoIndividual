SELECT count( * )FROM clientes;
SELECT COUNT(*) FROM COMPRA; 
SELECT * FROM COMPRA;
SELECT  distinct idProducto, count(distinct IdProducto), avg(Precio) promedio_Precio, precio 
FROM COMPRA GROUP BY IdProducto having IdProducto= 42754;

/*43043, 43037, 43036, 43035, 43034, 43032, 43030, 43012, 42969,42962*/

SELECT  IdCompra, fecha, idProducto, precio   FROM COMPRA where idProducto=  43037;
SELECT  IdCompra, fecha, idProducto, precio   FROM COMPRA where idCompra=  11175;
SELECT * FROM VENTA where idProducto =42754;
SELECT * FROM Gasto;
SELECT * FROM proveedores;
SELECT * FROM clientes;
SELECT * FROM LOCALIDADES;
select * from sucursales