var mysql = require('mysql');
var logger = require('./logger');
var moment = require('moment');

var reConnectCount = 0; // 重连次数统计
var dbConfig = {
    host: '192.168.1.196',
    port: 3306,
    user: 'root',
    password: 'ZWX#ztpms$7788',
    database: 'lianjia',
    multipleStatements: true
};

var connection = mysql.createConnection(dbConfig);

// 数据库链接
connection.connect(function(err) {
    if (err) {
        logger.debug('sql数据库连接失败：' + err.code);
        setTimeout(handleError, 2000);
        return;
    }
    logger.debug('sql数据库已连接：' + connection.threadId);
});

// 断线重连
connection.on('error', function(err) {
    logger.debug('sql数据库断线：' + err);
    if (err.code === 'PROTOCOL_CONNECTION_LOST') {
        handleError();
    } else {
        throw err;
    }
});

// 重连函数
function handleError() {
    if (reConnectCount >= 3) {
        logger.debug('sql数据库已重连3次，均失败，不再重连！');
        return;
    }
    reConnectCount++;
    connection = mysql.createConnection(dbConfig);
    connection.connect(function(err) {
        if (err) {
            logger.debug('sql数据库连接失败：' + err.code);
            setTimeout(handleError, 2000);
            return;
        }
        logger.debug('sql数据库已重连：', connection.threadId);
        reConnectCount = 0;
    });
    connection.on('error', function(err) {
        logger.debug('sql数据库断线：' + err);
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            handleError();
        } else {
            throw err;
        }
    });
}

// 基本查询函数
function query(sqlString, cb) {
    if (!cb || typeof query !== 'function') {
        logger.debug('查询回调不存在！直接返回');
        return;
    }
    connection.query(sqlString, function(error, results, fields) {
        cb(error, results);
    })
}

// 空函数，用于回调为空的情况
function nop() {}

/**基本查询函数
 * @param  {string}   sqlString sql语句
 * @param  {function} cb        回调
 * @return void
 */
exports.query = function(sqlString, cb) {
    query(sqlString, cb);
};
