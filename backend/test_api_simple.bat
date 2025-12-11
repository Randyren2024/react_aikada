@echo off
echo 正在测试打卡达人API...
echo ========================

echo.
echo 1. 测试健康检查端点:
curl -X GET http://localhost:5000/health
echo.

echo.
echo 2. 测试获取打卡记录:
curl -X GET "http://localhost:5000/api/checkins?user_id=1"
echo.

echo.
echo 3. 测试创建打卡记录:
curl -X POST http://localhost:5000/api/checkins -H "Content-Type: application/json" -d "{\"user_id\": \"1\", \"content\": \"测试打卡内容\", \"location\": \"测试地点\"}"
echo.

echo.
echo 4. 测试获取用户信息:
curl -X GET http://localhost:5000/api/users/1
echo.

echo.
echo 测试完成！
echo 如果以上测试都返回正常数据，说明API运行正常。
echo 如果仍然出现404错误，请检查服务器日志。
pause