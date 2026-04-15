"""
游泳记录 Web 应用 - Flask 后端
"""
from flask import Flask, render_template, request, jsonify
from data_manager import DataManager
import os

app = Flask(__name__)
data_manager = DataManager()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


# ==================== 用户管理 API ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户列表"""
    try:
        users = data_manager.get_all_usernames()
        return jsonify({'success': True, 'data': sorted(users)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users', methods=['POST'])
def add_user():
    """添加用户"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'success': False, 'message': '用户名不能为空'}), 400
        
        if username in data_manager.get_all_usernames():
            return jsonify({'success': False, 'message': '用户已存在'}), 400
        
        data_manager.get_or_create_user(username)
        return jsonify({'success': True, 'message': f'用户 {username} 添加成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    """删除用户"""
    try:
        success = data_manager.delete_user(username)
        if success:
            return jsonify({'success': True, 'message': f'用户 {username} 已删除'})
        else:
            return jsonify({'success': False, 'message': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 打卡 API ====================

@app.route('/api/records/<username>', methods=['GET'])
def get_records(username):
    """获取用户打卡记录"""
    try:
        records = data_manager.get_user_records(username)
        return jsonify({'success': True, 'data': records})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/records', methods=['POST'])
def add_record():
    """添加打卡记录"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        date = data.get('date', '').strip()
        sport_type = data.get('sport_type', 'swimming')
        sub_type = data.get('sub_type', '').strip() if data.get('sub_type') else None
        class_type = data.get('class_type', '').strip() if data.get('class_type') else None
        duration = data.get('duration', None)
        distance = data.get('distance', None)
        notes = data.get('notes', '').strip() if data.get('notes') else None
        
        if not username or not date:
            return jsonify({'success': False, 'message': '参数不完整'}), 400
        
        success, message = data_manager.add_record(username, date, sport_type, sub_type, class_type, duration, distance, notes)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 统计 API ====================

@app.route('/api/stats/<username>', methods=['GET'])
def get_stats(username):
    """获取用户统计信息"""
    try:
        sport_type = request.args.get('sport_type', None)
        time_range = request.args.get('time_range', 'all')
        stats = data_manager.get_user_stats(username, sport_type, time_range)
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/settings/<username>', methods=['PUT'])
def update_settings(username):
    """更新用户课时设置"""
    try:
        data = request.get_json()
        sport_type = data.get('sport_type', 'swimming')
        settings = {
            'total_classes': int(data.get('total_classes', 0)),
            'private_classes': int(data.get('private_classes', 0)),
            'card_classes': int(data.get('card_classes', 0))
        }
        
        data_manager.update_user_settings(username, settings, sport_type)
        return jsonify({'success': True, 'message': '设置已保存'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    print("🏊 游泳记录管理系统 - Web 版")
    print("=" * 50)
    print("访问地址: http://localhost:8989")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=8989)
