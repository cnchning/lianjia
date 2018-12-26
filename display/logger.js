const winston = require('winston');
const DailyRotateFile = require('winston-daily-rotate-file');
const format = winston.format;

// 文件配置
let options = {
    infoFile: {
        level: 'debug',
        filename: './logs/app-%DATE%.log',
        datePattern: 'YYYY-MM-DD',
        zippedArchive: false,
        handleExceptions: true,
        json: true,
        maxSize: '100m',
        maxFiles: '7d',
        colorize: false
    },
    errFile: {
        level: 'error',
        filename: './logs/err-%DATE%.log',
        datePattern: 'YYYY-MM-DD',
        zippedArchive: false,
        handleExceptions: true,
        json: true,
        maxSize: '100m',
        maxFiles: '7d',
        colorize: false
    },
    console: {
        level: 'debug',
        handleExceptions: true,
        json: false,
        colorize: true
    }
};

// 格式化数据
const myFormat = format.printf(info => {
        return `${info.timestamp} [${info.level}]: ${info.message}`;
});

// 日志对象
let logger = winston.createLogger({
    transports: [
        new winston.transports.DailyRotateFile(options.infoFile),
        new winston.transports.DailyRotateFile(options.errFile),
        new winston.transports.Console(options.console)
    ],
    format: format.combine(
        format.timestamp(),
        myFormat
    ),
    exitOnError: false
});

// 日志对象封装
let log = {};
log.info = function() {
    let content = '';
    for (let i = 0; i < arguments.length; i++) {
        if (arguments[i] instanceof Error) {
            content += arguments[i].stack + ' ';
            continue
        }

        if (typeof(arguments[i]) == 'object') {
            content += JSON.stringify(arguments[i]) + ' ';
            continue
        }

        content += arguments[i] + ' '
    }


    if (!content) {
        return
    }

    logger.info(content)
};
log.debug = function() {
    let content = '';
    for (let i = 0; i < arguments.length; i++) {
        if (arguments[i] instanceof Error) {
            content += arguments[i].stack + ' ';
            continue
        }

        if (typeof(arguments[i]) == 'object') {
            content += JSON.stringify(arguments[i]) + ' ';
            continue
        }

        content += arguments[i] + ' '
    }

    if (!content) {
        return
    }

    logger.debug(content)
};
log.error = function() {
    let content = '';
    for (let i = 0; i < arguments.length; i++) {
        if (arguments[i] instanceof Error) {
            content += '\r\n' + arguments[i].stack + ' ';
            continue
        }

        if (typeof(arguments[i]) == 'object') {
            content += JSON.stringify(arguments[i]) + ' ';
            continue
        }

        content += arguments[i] + ' '
    }

    if (!content) {
        return
    }

    logger.error(content)
};

module.exports = log;
