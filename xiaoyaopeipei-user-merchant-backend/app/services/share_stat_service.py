"""
分享统计服务
"""
import json
from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.share_stat import ShareStat
from app.models.conversation import Conversation
from app.models.lead import Lead


class ShareStatService:
    """分享统计服务类"""

    def get_by_merchant_and_date(
        self, db: Session, merchant_id: int, stat_date: date
    ) -> Optional[ShareStat]:
        """根据商家ID和日期获取统计记录"""
        return (
            db.query(ShareStat)
            .filter(
                ShareStat.merchant_id == merchant_id,
                ShareStat.date == stat_date,
            )
            .first()
        )

    def get_stats_by_period(
        self,
        db: Session,
        merchant_id: int,
        start_date: date,
        end_date: date,
    ) -> List[ShareStat]:
        """
        获取指定时间段的统计数据

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            统计记录列表
        """
        return (
            db.query(ShareStat)
            .filter(
                ShareStat.merchant_id == merchant_id,
                ShareStat.date >= start_date,
                ShareStat.date <= end_date,
            )
            .order_by(ShareStat.date.asc())
            .all()
        )

    def get_today_stat(self, db: Session, merchant_id: int) -> ShareStat:
        """
        获取或创建今日统计记录

        Args:
            db: 数据库会话
            merchant_id: 商家ID

        Returns:
            今日统计记录
        """
        today = date.today()

        # 尝试获取今日记录
        stat = self.get_by_merchant_and_date(db, merchant_id=merchant_id, stat_date=today)

        # 如果不存在，创建新记录
        if not stat:
            from app.utils.snowflake import generate_id

            stat = ShareStat(
                id=generate_id(),
                merchant_id=merchant_id,
                date=today,
                scan_count=0,
                consult_count=0,
                lead_count=0,
                device_type_stats=None,
                budget_stats=None,
            )
            db.add(stat)
            db.commit()
            db.refresh(stat)

        return stat

    def increment_scan_count(
        self, db: Session, merchant_id: int
    ) -> ShareStat:
        """
        增加扫码数

        Args:
            db: 数据库会话
            merchant_id: 商家ID

        Returns:
            更新后的统计记录
        """
        stat = self.get_today_stat(db, merchant_id=merchant_id)
        stat.scan_count += 1
        db.commit()
        db.refresh(stat)
        return stat

    def increment_consult_count(
        self,
        db: Session,
        merchant_id: int,
        device_type: Optional[str] = None,
        budget: Optional[str] = None,
    ) -> ShareStat:
        """
        增加咨询数（并记录设备类型和预算分布）

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            device_type: 设备类型
            budget: 预算

        Returns:
            更新后的统计记录
        """
        stat = self.get_today_stat(db, merchant_id=merchant_id)
        stat.consult_count += 1

        # 更新设备类型统计
        if device_type:
            device_stats = {}
            if stat.device_type_stats:
                try:
                    device_stats = json.loads(stat.device_type_stats)
                except:
                    pass

            device_stats[device_type] = device_stats.get(device_type, 0) + 1
            stat.device_type_stats = json.dumps(device_stats, ensure_ascii=False)

        # 更新预算分布统计
        if budget:
            budget_stats = {}
            if stat.budget_stats:
                try:
                    budget_stats = json.loads(stat.budget_stats)
                except:
                    pass

            # 预算区间分组
            budget_key = self._get_budget_key(budget)
            budget_stats[budget_key] = budget_stats.get(budget_key, 0) + 1
            stat.budget_stats = json.dumps(budget_stats, ensure_ascii=False)

        db.commit()
        db.refresh(stat)
        return stat

    def increment_lead_count(
        self, db: Session, merchant_id: int
    ) -> ShareStat:
        """
        增加线索数

        Args:
            db: 数据库会话
            merchant_id: 商家ID

        Returns:
            更新后的统计记录
        """
        stat = self.get_today_stat(db, merchant_id=merchant_id)
        stat.lead_count += 1
        db.commit()
        db.refresh(stat)
        return stat

    def _get_budget_key(self, budget: str) -> str:
        """
        将预算转换为区间Key

        Args:
            budget: 预算字符串

        Returns:
            预算区间Key
        """
        try:
            # 尝试解析数字
            budget = budget.replace("元", "").replace(" ", "").strip()

            if "-" in budget:
                # 区间形式：5000-8000
                parts = budget.split("-")
                min_val = int(parts[0])
                max_val = int(parts[1])

                if min_val < 5000:
                    return "5000以下"
                elif max_val <= 8000:
                    return "5000-8000"
                elif max_val <= 12000:
                    return "8000-12000"
                else:
                    return "12000以上"
            else:
                # 单个数字
                val = int(budget)
                if val < 5000:
                    return "5000以下"
                elif val <= 8000:
                    return "5000-8000"
                elif val <= 12000:
                    return "8000-12000"
                else:
                    return "12000以上"
        except:
            return "未知"

    def get_summary_stats(
        self,
        db: Session,
        merchant_id: int,
        period: str = "today",
    ) -> Dict[str, Any]:
        """
        获取汇总统计

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            period: 统计周期（today/week/month/all）

        Returns:
            汇总统计数据
        """
        today = date.today()
        yesterday = today - timedelta(days=1)

        # 确定日期范围
        if period == "today":
            start_date = today
            end_date = today
        elif period == "week":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "month":
            start_date = today - timedelta(days=30)
            end_date = today
        else:  # all
            start_date = None
            end_date = None

        # 查询当前周期统计数据
        query = db.query(ShareStat).filter(ShareStat.merchant_id == merchant_id)

        if start_date and end_date:
            query = query.filter(
                ShareStat.date >= start_date,
                ShareStat.date <= end_date,
            )

        stats_list = query.all()

        # 汇总数据
        total_scan = sum(s.scan_count for s in stats_list)
        total_consult = sum(s.consult_count for s in stats_list)
        total_lead = sum(s.lead_count for s in stats_list)

        # 合并设备类型统计
        device_type_stats = {}
        for stat in stats_list:
            if stat.device_type_stats:
                try:
                    stats = json.loads(stat.device_type_stats)
                    for key, value in stats.items():
                        device_type_stats[key] = device_type_stats.get(key, 0) + value
                except:
                    pass

        # 合并预算统计
        budget_stats = {}
        for stat in stats_list:
            if stat.budget_stats:
                try:
                    stats = json.loads(stat.budget_stats)
                    for key, value in stats.items():
                        budget_stats[key] = budget_stats.get(key, 0) + value
                except:
                    pass

        # 计算转化率（线索数/咨询数）
        conversion_rate = 0.0
        if total_consult > 0:
            conversion_rate = round((total_lead / total_consult) * 100, 2) / 100

        # ========== 计算趋势（较昨日） ==========
        # 只在今日统计时计算趋势
        consult_trend = 0
        lead_trend = 0
        conversion_trend = 0

        if period == "today":
            # 获取昨日数据
            yesterday_stats = self.get_by_merchant_and_date(db, merchant_id, yesterday)

            if yesterday_stats:
                # 计算咨询数趋势: (今日 - 昨日) / 昨日 × 100
                if yesterday_stats.consult_count > 0:
                    consult_trend = round(
                        ((total_consult - yesterday_stats.consult_count) / yesterday_stats.consult_count) * 100, 2
                    )
                elif total_consult > 0:
                    consult_trend = 100.0  # 昨日0，今日有数据，增长100%

                # 计算线索数趋势
                if yesterday_stats.lead_count > 0:
                    lead_trend = round(
                        ((total_lead - yesterday_stats.lead_count) / yesterday_stats.lead_count) * 100, 2
                    )
                elif total_lead > 0:
                    lead_trend = 100.0

                # 计算转化率趋势
                yesterday_conversion_rate = 0.0
                if yesterday_stats.consult_count > 0:
                    yesterday_conversion_rate = round(
                        (yesterday_stats.lead_count / yesterday_stats.consult_count) * 100, 2
                    ) / 100

                if yesterday_conversion_rate > 0:
                    conversion_trend = round(
                        ((conversion_rate - yesterday_conversion_rate) / yesterday_conversion_rate) * 100, 2
                    )
                elif conversion_rate > 0:
                    conversion_trend = 100.0

        return {
            "scan_count": total_scan,
            "consult_count": total_consult,
            "lead_count": total_lead,
            "conversion_rate": conversion_rate,
            "consult_trend": consult_trend,
            "lead_trend": lead_trend,
            "conversion_trend": conversion_trend,
            "device_type_stats": device_type_stats,
            "budget_stats": budget_stats,
        }

    def get_trend_stats(
        self,
        db: Session,
        merchant_id: int,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        """
        获取趋势统计（最近N天）

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            days: 天数

        Returns:
            每日统计数据列表
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        stats_list = self.get_stats_by_period(
            db=db,
            merchant_id=merchant_id,
            start_date=start_date,
            end_date=end_date,
        )

        # 创建日期映射
        stats_map = {s.date: s for s in stats_list}

        # 填充缺失日期
        result = []
        current_date = start_date
        while current_date <= end_date:
            stat = stats_map.get(current_date)
            if stat:
                result.append({
                    "date": current_date.isoformat(),
                    "scan_count": stat.scan_count,
                    "consult_count": stat.consult_count,
                    "lead_count": stat.lead_count,
                })
            else:
                result.append({
                    "date": current_date.isoformat(),
                    "scan_count": 0,
                    "consult_count": 0,
                    "lead_count": 0,
                })
            current_date += timedelta(days=1)

        return result


# 创建服务实例
share_stat_service = ShareStatService()
