var express = require('express');
var mysql = require('../mysql');
var logger = require('../logger');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  mysql.query('select ymd, num_priceup as up, num_pricedown as down, num_pricedown+num_priceup as total,num_house as nh from maininfo order by ymd limit 60', function (err, data) {
      logger.debug(data);
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

router.post('/getdstcpr', function(req, res, next) {
    var sql = 'SELECT a.district, a.nh, cast(a.avgtotal as DECIMAL(10,2)) as avgtotal, cast(a.avgunit as DECIMAL(10,2)) as avgunit, IFNULL(b.numup,0) as numup, IFNULL(c.numdown,0) as numdown,cast(d.hot/a.nh as DECIMAL(10,2))*100 as hot from' +
        '    (SELECT district,sum(num_house) as nh, sum(total_price)/count(0) as avgtotal, sum(unit_price)/count(0) as avgunit from avgDistrict where ymd=DATE_FORMAT(NOW(),\'%Y%m%d\')-1 group by district) as a' +
        '    LEFT JOIN (select district, count(0) as numup from houseA inner JOIN pricelog on houseA.id=pricelog.id and DATEDIFF(pricelog.createDate,NOW())=-1 and pricetrend=\'up\'	GROUP BY district) as b on a.district=b.district' +
        '    LEFT JOIN (select district, count(0) as numdown from houseA inner JOIN pricelog on houseA.id=pricelog.id and DATEDIFF(pricelog.createDate,NOW())=-1 and pricetrend=\'down\'	GROUP BY district) as c on a.district=c.district' +
        '    LEFT JOIN (select district,(sum(follow)+sum(take_look)*7) as hot from houseA where DATEDIFF(NOW(),touchTime)=1 group by district) as d on a.district=d.district' +
        '    order by hot desc;';
    sql += "SELECT concat(a.bedroom_num,'居室') as bn, a.nh, cast(a.area as DECIMAL(10,2)) as area,cast(a.avgtotal as DECIMAL(10,2)) as avgtotal, cast(a.avgunit as DECIMAL(10,2)) as avgunit, IFNULL(b.numup,0) as numup, IFNULL(c.numdown,0) as numdown,cast(d.hot/a.nh as DECIMAL(10,2))*100 as hot from " +
        "   (SELECT bedroom_num,sum(num_house) as nh, sum(build_area)/count(0) as area, sum(total_price)/count(0) as avgtotal, sum(unit_price)/count(0) as avgunit from avgDistrict where bedroom_num>0 and ymd=DATE_FORMAT(NOW(),'%Y%m%d')-1 group by bedroom_num) as a" +
        "   LEFT JOIN (select bedroom_num, count(0) as numup from houseA inner JOIN pricelog on houseA.id=pricelog.id and DATEDIFF(pricelog.createDate,NOW())=-1 and pricetrend='up'	GROUP BY bedroom_num) as b on a.bedroom_num=b.bedroom_num" +
        "   LEFT JOIN (select bedroom_num, count(0) as numdown from houseA inner JOIN pricelog on houseA.id=pricelog.id and DATEDIFF(pricelog.createDate,NOW())=-1 and pricetrend='down'	GROUP BY bedroom_num) as c on a.bedroom_num=c.bedroom_num " +
        "   LEFT JOIN (select bedroom_num,(sum(follow)+sum(take_look)*7) as hot from houseA where DATEDIFF(NOW(),touchTime)=1 group by bedroom_num) as d on a.bedroom_num=d.bedroom_num" +
        "   order by bn;";
    logger.debug('/getdstcpr.sql: ' + sql);
    mysql.query(sql, function (err, data) {
        if(!data) return false;
        var obj = {}, districtData=data[0], bedroomData = data[1];
        obj.y = [], obj.data=[];
        for(var i=0;i<districtData.length;i++) {
            obj.y.push(districtData[i].district);
            obj.data.push({
                district: districtData[i].district,
                val: [districtData[i].nh, districtData[i].numdown, districtData[i].numup, districtData[i].hot, districtData[i].avgtotal, districtData[i].avgunit]
            });
        }
        obj.b = [],obj.bdata = [];
        for(var i=0;i<bedroomData.length;i++) {
            obj.b.push(bedroomData[i].bn);
            obj.bdata.push({
                bn: bedroomData[i].bn,
                val: [bedroomData[i].nh, bedroomData[i].numdown, bedroomData[i].numup, bedroomData[i].area, bedroomData[i].hot, bedroomData[i].avgtotal, bedroomData[i].avgunit]
            });
        }
        logger.debug(obj);
        res.write(JSON.stringify(obj));
        res.end();
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
