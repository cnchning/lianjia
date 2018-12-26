var express = require('express');
var mysql = require('../mysql');
var logger = require('../logger');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  mysql.query('select ymd, num_priceup as up, num_pricedown as down, num_pricedown+num_priceup as total,num_house as nh from maininfo order by ymd limit 60', function (err, data) {
      // logger.debug(data);
      var x=[],ytotal=[],ydown=[],yup=[], nh=data[data.length-1].nh;
      for(var i=0;i<data.length;i++){
          x.push(data[i].ymd);
          ytotal.push(data[i].total);
          yup.push(data[i].up);
          ydown.push(data[i].down);
      }

      res.render('index', { title: '走势',x:x, ytotal:ytotal, ydown:ydown, yup:yup, nh: nh });
  });
});

router.post('/getdap', function(req, res, next) {
    var districts = req.body['district[]'];
    districts = districts.join('\',\'');
    var dt = req.body.dt, sql;
    if(dt=='week') {
        sql = 'select ymd, district as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgDistrict' +
            ' where district in (\'' + districts + '\') and ymd%7=(DATE_FORMAT(NOW(),\'%Y%m%d\')-1)%7 group by ymd,ds' +
            '    UNION' +
            '    SELECT ymd,\'全成都\' as ds, avg_unit_price as dp from maininfo where ymd%7=(DATE_FORMAT(NOW(),\'%Y%m%d\')-1)%7' +
            '    order by ymd';
    } else {
        sql = 'select ymd, district as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgDistrict' +
            ' where district in (\'' + districts + '\') group by ymd,ds' +
            '    UNION' +
            '    SELECT ymd,\'全成都\' as ds, avg_unit_price as dp from maininfo' +
            '    order by ymd';
    }
    logger.debug('/getdap.sql: ' + sql);
    mysql.query(sql, function (err, data) {
        // logger.debug(data);
        if(!data) return false;
        var obj = {};
        obj.x = [], obj.y = [], obj.data={};
        for(var i=0;i<data.length;i++) {
          if(obj.x.indexOf(data[i].ymd) == -1)
              obj.x.push(data[i].ymd);
          if(obj.y.indexOf(data[i].ds) == -1) {
              obj.y.push(data[i].ds);
              obj.data[data[i].ds] = [];
          }
          obj.data[data[i].ds].push(data[i].dp);
        }
        logger.debug(obj);
        res.write(JSON.stringify(obj));
        res.end();
    });
});

router.post('/getpap', function(req, res, next) {
    var positions = req.body['position[]'];
    positions = positions.join('\',\'');
    var dt = req.body.dt, sql;
    if(dt=='week') {
        sql = 'select ymd, position as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgPosition' +
            ' where position in (\'' + positions + '\') and ymd%7=(DATE_FORMAT(NOW(),\'%Y%m%d\')-1)%7 group by ymd,ds' +
            '    order by ymd';
    } else {
        sql = 'select ymd, position as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgPosition' +
            ' where position in (\'' + positions + '\') group by ymd,ds' +
            '    order by ymd';
    }
    logger.debug('/getpap.sql: ' + sql);
    mysql.query(sql, function (err, data) {
        // logger.debug(data);
        if(!data) return false;
        var obj = {};
        obj.x = [], obj.y = [], obj.data={};
        for(var i=0;i<data.length;i++) {
            if(obj.x.indexOf(data[i].ymd) == -1)
                obj.x.push(data[i].ymd);
            if(obj.y.indexOf(data[i].ds) == -1) {
                obj.y.push(data[i].ds);
                obj.data[data[i].ds] = [];
            }
            obj.data[data[i].ds].push(data[i].dp);
        }
        logger.debug(obj);
        res.write(JSON.stringify(obj));
        res.end();
    });
});

router.post('/geteap', function(req, res, next) {
    var estates = req.body['estate[]'];
    estates = estates.join('\',\'');
    var dt = req.body.dt, sql;
    if(dt=='week') {
        sql = 'select ymd, housing_estate as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgEstate' +
            ' where housing_estate in (\'' + estates + '\') and ymd%7=(DATE_FORMAT(NOW(),\'%Y%m%d\')-1)%7 group by ymd,ds' +
            '    order by ymd';
    } else {
        sql = 'select ymd, housing_estate as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgEstate' +
            ' where housing_estate in (\'' + estates + '\') group by ymd,ds' +
            '    order by ymd';
    }
    logger.debug('/geteap.sql: ' + sql);
    mysql.query(sql, function (err, data) {
        // logger.debug(data);
        if(!data) return false;
        var obj = {};
        obj.x = [], obj.y = [], obj.data={};
        for(var i=0;i<data.length;i++) {
            if(obj.x.indexOf(data[i].ymd) == -1)
                obj.x.push(data[i].ymd);
            if(obj.y.indexOf(data[i].ds) == -1) {
                obj.y.push(data[i].ds);
                obj.data[data[i].ds] = [];
            }
            obj.data[data[i].ds].push(data[i].dp);
        }
        logger.debug(obj);
        res.write(JSON.stringify(obj));
        res.end();
    });
});

router.post('/getbap', function(req, res, next) {
    var districts = req.body['district[]'];
    districts = districts.join('\',\'');
    var dt = req.body.dt, sql;
    if(dt=='week') {
        sql = 'select ymd, concat(bedroom_num, \'居室\') as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgDistrict' +
            ' where bedroom_num>0 and ymd%7=(DATE_FORMAT(NOW(),\'%Y%m%d\')-1)%7 group by ymd,ds' +
            '    order by ymd';
    } else {
        sql = 'select ymd, concat(bedroom_num, \'居室\') as ds, cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as dp from avgDistrict' +
            ' where bedroom_num>0 group by ymd,ds' +
            '    order by ymd';
    }
    logger.debug('/getbap.sql: ' + sql);
    mysql.query(sql, function (err, data) {
        // logger.debug(data);
        if(!data) return false;
        var obj = {};
        obj.x = [], obj.y = [], obj.data={};
        for(var i=0;i<data.length;i++) {
            if(obj.x.indexOf(data[i].ymd) == -1)
                obj.x.push(data[i].ymd);
            if(obj.y.indexOf(data[i].ds) == -1) {
                obj.y.push(data[i].ds);
                obj.data[data[i].ds] = [];
            }
            obj.data[data[i].ds].push(data[i].dp);
        }
        logger.debug(obj);
        res.write(JSON.stringify(obj));
        res.end();
    });
});

module.exports = router;
