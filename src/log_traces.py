# log_traces.py
import sqlite3
from datetime import datetime
from contextlib import contextmanager

class QueryLogger:
    """쿼리 로깅 관리 클래스"""
    
    DB_PATH = "query_logs.db"
    
    @staticmethod
    def init_db():
        """DB 초기화"""
        conn = sqlite3.connect(QueryLogger.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_query TEXT,
                generated_sql TEXT,
                execution_time REAL,
                result_rows INTEGER,
                error_message TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    @staticmethod
    def save_log(user_query, generated_sql, execution_time=None, result_rows=None, error_msg=None):
        """로그 저장"""
        conn = sqlite3.connect(QueryLogger.DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO query_logs 
            (timestamp, user_query, generated_sql, execution_time, result_rows, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, user_query, generated_sql, execution_time, result_rows, error_msg))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_logs():
        """모든 로그 조회"""
        conn = sqlite3.connect(QueryLogger.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM query_logs')
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    @staticmethod
    @contextmanager
    def log_execution(user_query):
        """Context manager로 자동 시간 측정 & 로깅"""
        import time
        start_time = time.time()
        
        try:
            yield
        except Exception as e:
            execution_time = time.time() - start_time
            QueryLogger.save_log(user_query, None, execution_time, None, str(e))
            raise

# 테스트
QueryLogger.init_db()
with QueryLogger.log_execution("SELECT * FROM albums"):
    # 쿼리 실행 코드 (예: execute_sql("SELECT * FROM albums"))
    pass
logs = QueryLogger.get_all_logs()
print('[info] logs 저장 예시:\n', logs)    