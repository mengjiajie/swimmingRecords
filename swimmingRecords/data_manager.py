"""
数据管理模块 - 负责用户信息和打卡记录的读写操作
"""
import json
import os
from datetime import datetime


class DataManager:
    """数据管理类，处理所有数据的持久化操作"""
    
    def __init__(self, data_file="swimming_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self):
        """从JSON文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
                return {"users": {}}
        return {"users": {}}
    
    def _save_data(self):
        """保存数据到JSON文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def get_or_create_user(self, username):
        """获取或创建用户"""
        if username not in self.data["users"]:
            self.data["users"][username] = {
                "records": [],
                "settings": {
                    "swimming": {
                        "total_classes": 0,
                        "private_classes": 0,
                        "card_classes": 0
                    },
                    "fitness": {
                        "total_classes": 0,
                        "private_classes": 0,
                        "card_classes": 0
                    },
                    "running": {
                        "total_classes": 0,
                        "private_classes": 0,
                        "card_classes": 0
                    }
                }
            }
            self._save_data()
        return self.data["users"][username]
    
    def add_record(self, username, date, sport_type, sub_type=None, class_type=None, duration=None, distance=None, notes=None):
        """添加打卡记录
        
        Args:
            username: 用户名
            date: 打卡日期 (YYYY-MM-DD)
            sport_type: 运动类型 ('swimming' 游泳, 'fitness' 健身, 'running' 跑步等)
            sub_type: 子类型 (可选，如泳种、健身项目等)
            class_type: 课程类型 (可选，如私教课、次卡)
            duration: 运动时长（分钟，可选）
            distance: 运动距离（米/公里，可选）
            notes: 备注（可选）
        """
        user = self.get_or_create_user(username)
        
        # 检查是否已经存在该日期的该运动类型记录
        for record in user["records"]:
            if record["date"] == date and record["sport_type"] == sport_type:
                return False, "该日期已有此运动类型的打卡记录"
        
        # 添加新记录
        record = {
            "date": date,
            "sport_type": sport_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 添加可选字段
        if sub_type:
            record["sub_type"] = sub_type
        if class_type:
            record["class_type"] = class_type
        if duration:
            record["duration"] = duration
        if distance:
            record["distance"] = distance
        if notes:
            record["notes"] = notes
        
        user["records"].append(record)
        
        self._save_data()
        return True, "打卡成功"
    
    def get_user_records(self, username):
        """获取用户的所有打卡记录"""
        user = self.get_or_create_user(username)
        return sorted(user["records"], key=lambda x: x["date"], reverse=True)
    
    def get_user_stats(self, username, sport_type=None, time_range='all'):
        """获取用户统计信息
        
        Args:
            username: 用户名
            sport_type: 运动类型（可选），如果不指定则统计所有类型
            time_range: 时间范围 ('week', 'month', 'year', 'all')
        """
        user = self.get_or_create_user(username)
        records = user["records"]
        
        # 如果指定了运动类型，过滤记录
        if sport_type:
            records = [r for r in records if r.get("sport_type") == sport_type]
        
        # 根据时间范围过滤记录（使用打卡日期，按自然周/月/年计算）
        from datetime import datetime, timedelta
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        if time_range == 'week':
            # 本周一开始
            weekday = now.weekday()  # 0=周一, 6=周日
            monday = (now - timedelta(days=weekday)).replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff = monday.strftime("%Y-%m-%d")
            records = [r for r in records if r["date"] >= cutoff]
        elif time_range == 'month':
            # 本月1号开始
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            cutoff = first_day.strftime("%Y-%m-%d")
            records = [r for r in records if r["date"] >= cutoff]
        elif time_range == 'year':
            # 本年1月1号开始
            first_day = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            cutoff = first_day.strftime("%Y-%m-%d")
            records = [r for r in records if r["date"] >= cutoff]
        
        # 统计总记录数
        total_count = len(records)
        
        # 统计总时长
        total_duration = sum(r.get("duration", 0) for r in records if r.get("duration"))
        
        # 统计总距离
        total_distance = sum(r.get("distance", 0) for r in records if r.get("distance"))
        
        # 统计各子类型的次数
        sub_type_stats = {}
        for r in records:
            sub_type = r.get("sub_type")
            if sub_type:
                sub_type_stats[sub_type] = sub_type_stats.get(sub_type, 0) + 1
        
        # 统计私教课和次卡次数
        private_count = sum(1 for r in records if r.get("class_type") == "私教课")
        card_count = sum(1 for r in records if r.get("class_type") == "次卡")
        
        # 按日期和课程类型分类用于趋势分析
        dates_set = set()
        class_type_data = {}  # 各课程类型
        
        for r in records:
            date = r["date"]
            dates_set.add(date)
            class_type = r.get("class_type") or "其他"  # 没有课程类型的归为"其他"
            
            if class_type not in class_type_data:
                class_type_data[class_type] = {}
            
            if date not in class_type_data[class_type]:
                class_type_data[class_type][date] = 0
            class_type_data[class_type][date] += 1
        
        # 生成趋势数据（按日期排序）
        sorted_dates = sorted(list(dates_set))
        trend_data = {
            "dates": sorted_dates,
            "series": []
        }
        
        for class_type, date_counts in class_type_data.items():
            series_data = []
            for date in sorted_dates:
                series_data.append({
                    "date": date,
                    "count": date_counts.get(date, 0)
                })
            trend_data["series"].append({
                "name": class_type,
                "data": series_data
            })
        
        # 确保settings格式正确（按运动类型分离）
        settings = user["settings"]
        if not isinstance(settings, dict) or "swimming" not in settings:
            # 旧数据格式兼容：转换为新格式
            settings = {
                "swimming": {
                    "total_classes": settings.get("total_classes", 0) if isinstance(settings, dict) else 0,
                    "private_classes": settings.get("private_classes", 0) if isinstance(settings, dict) else 0,
                    "card_classes": settings.get("card_classes", 0) if isinstance(settings, dict) else 0
                },
                "fitness": {
                    "total_classes": 0,
                    "private_classes": 0,
                    "card_classes": 0
                },
                "running": {
                    "total_classes": 0,
                    "private_classes": 0,
                    "card_classes": 0
                }
            }
            user["settings"] = settings
            self._save_data()
        
        return {
            "total_count": total_count,
            "total_duration": total_duration,
            "total_distance": total_distance,
            "private_count": private_count,
            "card_count": card_count,
            "sub_type_stats": sub_type_stats,
            "trend_data": trend_data,
            "settings": settings
        }
    
    def update_user_settings(self, username, settings, sport_type):
        """更新用户设置
        
        Args:
            username: 用户名
            settings: 设置字典，包含 total_classes, private_classes, card_classes
            sport_type: 运动类型（swimming/fitness/running）
        """
        user = self.get_or_create_user(username)
        if sport_type not in user["settings"]:
            user["settings"][sport_type] = {
                "total_classes": 0,
                "private_classes": 0,
                "card_classes": 0
            }
        user["settings"][sport_type].update(settings)
        self._save_data()
    
    def delete_user(self, username):
        """删除用户及其所有记录"""
        if username in self.data["users"]:
            del self.data["users"][username]
            self._save_data()
            return True
        return False
    
    def get_all_usernames(self):
        """获取所有用户名列表"""
        return list(self.data["users"].keys())
