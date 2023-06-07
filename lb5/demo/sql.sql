/*
  2023-06-07 16:30
  用户: FxDr
  服务器: FXX-LEGION
  数据库: OS
  应用程序: OS 
*/
CREATE TABLE Message
(
    id        INT IDENTITY(1,1) PRIMARY KEY,
    sender    VARCHAR(255) NOT NULL,
    receiver  VARCHAR(255) NOT NULL,
    message   TEXT         NOT NULL,
    timestamp DATETIME DEFAULT GETDATE()
);
