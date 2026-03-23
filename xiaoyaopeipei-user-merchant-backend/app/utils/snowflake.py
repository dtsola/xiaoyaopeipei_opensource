"""
雪花算法ID生成器
"""
import time
import threading
from typing import Optional


class SnowflakeIDGenerator:
    """
    雪花算法ID生成器
    """

    def __init__(self, datacenter_id: int = 1, worker_id: int = 1):
        """
        初始化

        Args:
            datacenter_id: 数据中心ID（0-31）
            worker_id: 机器ID（0-31）
        """
        # 起始时间戳（2020-01-01 00:00:00）
        self.epoch = 1577808000000

        # 各部分位数
        self.datacenter_id_bits = 5
        self.worker_id_bits = 5
        self.sequence_bits = 12

        # 最大值
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)  # 31
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)  # 31
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)  # 4095

        # 位移
        self.worker_id_shift = self.sequence_bits  # 12
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits  # 17
        self.timestamp_shift = (
            self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        )  # 22

        # 验证参数
        if datacenter_id > self.max_datacenter_id or datacenter_id < 0:
            raise ValueError(
                f"datacenter_id must be between 0 and {self.max_datacenter_id}"
            )
        if worker_id > self.max_worker_id or worker_id < 0:
            raise ValueError(f"worker_id must be between 0 and {self.max_worker_id}")

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_millis(self) -> int:
        """获取当前毫秒时间戳"""
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待下一毫秒"""
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    def generate_id(self) -> int:
        """
        生成雪花ID

        Returns:
            20位整数ID
        """
        with self.lock:
            timestamp = self._current_millis()

            # 时钟回拨检测
            if timestamp < self.last_timestamp:
                raise Exception(
                    f"Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} milliseconds"
                )

            # 同一毫秒内
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    # 序列号用完，等待下一毫秒
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 新的毫秒，序列号重置
                self.sequence = 0

            self.last_timestamp = timestamp

            # 组装ID
            snowflake_id = (
                ((timestamp - self.epoch) << self.timestamp_shift)
                | (self.datacenter_id << self.datacenter_id_shift)
                | (self.worker_id << self.worker_id_shift)
                | self.sequence
            )

            return snowflake_id


# 全局ID生成器实例
id_generator = SnowflakeIDGenerator(datacenter_id=1, worker_id=1)


def generate_id() -> int:
    """
    生成雪花ID

    Returns:
        20位整数ID

    Example:
        >>> generate_id()
        1734857600000000001
    """
    return id_generator.generate_id()
