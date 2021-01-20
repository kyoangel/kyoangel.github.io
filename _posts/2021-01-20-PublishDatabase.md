---
layout: post
author: Kyo
title:  "解決 Database 專案 發佈到 SQL Server 的問題"
image: assets/images/troubleshoot/publishsqlserver.png
featured: false
categories: troubleshoot
---

如果你在 DB 專案中使用 db.publish.xml 結果失敗且錯誤訊息類似於
`The target table 'j' of the DML statement cannot have any enabled triggers if the statement contains an OUTPUT clause without INTO claus.`
這是因為資料表有設定 trigger，而發佈的資料不會被同步，因此失敗。

我的解決方案是，參考[官方文件][outlink]{:target="_blank"}暫時停掉所有的資料表的 trigger。

步驟1: 首先建立一個預存程序 (stored procedure)
``` sql
CREATE PROCEDURE pr_Disable_Triggers 
@disable BIT = 1
AS 
    DECLARE
        @sql VARCHAR(500),
        @tableName VARCHAR(128),
        @triggerName VARCHAR(128),
        @tableSchema VARCHAR(128)

    -- List of all triggers and tables that exist on them
    DECLARE triggerCursor CURSOR
        FOR
    SELECT
        so_tr.name AS TriggerName,
        so_tbl.name AS TableName,
        t.TABLE_SCHEMA AS TableSchema
    FROM
        sysobjects so_tr
    INNER JOIN sysobjects so_tbl ON so_tr.parent_obj = so_tbl.id
    INNER JOIN INFORMATION_SCHEMA.TABLES t 
    ON 
        t.TABLE_NAME = so_tbl.name
    WHERE
        so_tr.type = 'TR'
    ORDER BY
        so_tbl.name ASC,
        so_tr.name ASC

    OPEN triggerCursor

    FETCH NEXT FROM triggerCursor 
    INTO @triggerName, @tableName, @tableSchema

    WHILE ( @@FETCH_STATUS = 0 )
        BEGIN
            IF @disable = 1 
                SET @sql = 'DISABLE TRIGGER [' 
                    + @triggerName + '] ON ' 
                    + @tableSchema + '.[' + @tableName + ']'
            ELSE 
                SET @sql = 'ENABLE TRIGGER [' 
                    + @triggerName + '] ON ' 
                    + @tableSchema + '.[' + @tableName + ']'

            PRINT 'Executing Statement - ' + @sql
            EXECUTE ( @sql )
            FETCH NEXT FROM triggerCursor 
            INTO @triggerName, @tableName,  @tableSchema
        END

    CLOSE triggerCursor
    DEALLOCATE triggerCursor
```
步驟2: 執行這個預存程序
`pr_Disable_Triggers 1`

你會看到類似於 
`Executing Statement - DISABLE TRIGGER [TriggerName] ON dbo.[TableName]` 的訊息

然後再次發佈 db.publish.xml 就成功啦，想要再次啟用 trigger 也只要執行 `pr_Disable_Triggers 0` 就可以啦~

Problem solve。

[outlink]: https://docs.microsoft.com/en-us/archive/msdn-magazine/2007/april/data-points-disabling-constraints-and-triggers