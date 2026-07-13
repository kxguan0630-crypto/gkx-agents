"""
Tool definitions for the dental business AI agent.
These are the external tools that the agent can call.
"""

from typing import Any, Dict


class DentalTools:
    """牙科业务工具集合"""
    
    @staticmethod
    def get_patients_by_name_and_phone(name: str, phone: str) -> Dict[str, Any]:
        """
        根据姓名和手机号查询患者
        
        输入:
            name: 患者姓名
            phone: 患者手机号
            
        输出:
            {
                "exists": bool,           # 患者是否存在
                "patient_code": str       # 患者代码（如果存在）
            }
        """
        pass
    
    @staticmethod
    def case_add(patient_code: str) -> Dict[str, Any]:
        """
        创建病例
        
        输入:
            patient_code: 患者代码
            
        输出:
            {
                "case_code": str          # 创建的病例代码
            }
        """
        pass
    
    @staticmethod
    def get_product_list() -> Dict[str, Any]:
        """
        获取产品列表
        
        输出:
            {
                "products": [
                    {
                        "product_id": str,
                        "name": str,
                        "price": float,
                        "description": str
                    },
                    ...
                ]
            }
        """
        pass
    
    @staticmethod
    def case_order_add(
        patient_code: str,
        case_code: str,
        products: list,
        total_price: float,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        创建订单
        
        输入:
            patient_code: 患者代码
            case_code: 病例代码
            products: 产品列表
            total_price: 总价
            notes: 备注
            
        输出:
            {
                "order_code": str,        # 创建的订单代码
                "success": bool
            }
        """
        pass
