import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from typing import List, Dict, Optional

class PriceComparator:
    def __init__(self):
        # 设置请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_price(self, url: str) -> Optional[float]:
        """
        从给定的URL获取商品价格
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试不同的价格提取方法
            # 方法1：查找包含价格的meta标签
            meta_price = soup.find('meta', {'property': 'product:price:amount'})
            if meta_price and meta_price.get('content'):
                return float(meta_price['content'])
            
            # 方法2：查找常见的价格类名
            price_classes = ['price', 'product-price', 'price-value', 'final-price']
            for class_name in price_classes:
                price_element = soup.find(class_=class_name)
                if price_element:
                    price_text = price_element.get_text()
                    price = self.extract_price_from_text(price_text)
                    if price:
                        return price
            
            # 方法3：使用正则表达式在整个页面中搜索价格
            price_pattern = r'[\$€¥£]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*[\$€¥£]?'
            matches = re.findall(price_pattern, response.text)
            if matches:
                # 过滤并转换所有找到的价格，取最小的（可能促销价最低）
                prices = []
                for match in matches:
                    price = self.extract_price_from_text(match)
                    if price:
                        prices.append(price)
                if prices:
                    return min(prices)
            
            return None
            
        except Exception as e:
            print(f"获取价格时出错: {e}")
            return None
    
    def extract_price_from_text(self, text: str) -> Optional[float]:
        """
        从文本中提取价格数字
        """
        try:
            # 移除货币符号和千位分隔符
            cleaned = re.sub(r'[^\d.,]', '', text)
            # 处理不同地区的小数分隔符
            if ',' in cleaned and '.' in cleaned:
                # 如果两者都有，最后一个作为小数点
                if cleaned.rindex(',') > cleaned.rindex('.'):
                    cleaned = cleaned.replace('.', '').replace(',', '.')
                else:
                    cleaned = cleaned.replace(',', '')
            elif ',' in cleaned:
                # 只有逗号，可能是欧洲格式或千位分隔符
                if cleaned.count(',') == 1 and len(cleaned.split(',')[1]) == 2:
                    # 可能是欧洲小数格式
                    cleaned = cleaned.replace(',', '.')
                else:
                    # 可能是千位分隔符
                    cleaned = cleaned.replace(',', '')
            
            return float(cleaned)
        except:
            return None
    
    def compare_prices(self, product_urls: Dict[str, List[str]]) -> Dict[str, Dict]:
        """
        比较多个平台上相似商品的价格
        :param product_urls: 字典，键是平台名称，值是该平台上商品URL列表
        :return: 包含比较结果的字典
        """
        results = {}
        
        for platform, urls in product_urls.items():
            platform_prices = []
            for url in urls:
                print(f"正在从 {platform} 获取价格: {url}")
                price = self.fetch_price(url)
                if price:
                    platform_prices.append(price)
            
            if platform_prices:
                results[platform] = {
                    'min_price': min(platform_prices),
                    'avg_price': sum(platform_prices) / len(platform_prices),
                    'max_price': max(platform_prices),
                    'num_products': len(platform_prices)
                }
        
        # 找出所有平台中的最低价
        if results:
            all_prices = [(platform, data['min_price']) for platform, data in results.items()]
            cheapest_platform, cheapest_price = min(all_prices, key=lambda x: x[1])
            results['cheapest'] = {
                'platform': cheapest_platform,
                'price': cheapest_price
            }
        
        return results
    
    def print_comparison_results(self, results: Dict[str, Dict]):
        """
        打印价格比较结果
        """
        if not results:
            print("没有获取到有效的价格数据")
            return
        
        print("\n=== 价格比较结果 ===")
        for platform, data in results.items():
            if platform == 'cheapest':
                continue
            print(f"\n平台: {platform}")
            print(f"  最低价: ${data['min_price']:.2f}")
            print(f"  平均价: ${data['avg_price']:.2f}")
            print(f"  最高价: ${data['max_price']:.2f}")
            print(f"  商品数量: {data['num_products']}")
        
        if 'cheapest' in results:
            cheapest = results['cheapest']
            print(f"\n★ 最低价来自 {cheapest['platform']}: ${cheapest['price']:.2f}")

# 使用示例
if __name__ == "__main__":
    # 示例商品URL（实际使用时替换为真实URL）
    product_urls = {
        "Amazon": [
            "https://www.amazon.com/dp/B08N5KWB9H",
            "https://www.amazon.com/dp/B08N5KWB9H"
        ],
        "eBay": [
            "https://www.ebay.com/itm/22445678901",
            "https://www.ebay.com/itm/22445678902"
        ],
        "Walmart": [
            "https://www.walmart.com/ip/12345678",
            "https://www.walmart.com/ip/12345679"
        ]
    }
    
    comparator = PriceComparator()
    results = comparator.compare_prices(product_urls)
    comparator.print_comparison_results(results)
    
    # 可选：将结果保存为CSV
    if results and 'cheapest' in results:
        df_data = []
        for platform, data in results.items():
            if platform == 'cheapest':
                continue
            df_data.append({
                'Platform': platform,
                'Min Price': data['min_price'],
                'Avg Price': data['avg_price'],
                'Max Price': data['max_price'],
                'Number of Products': data['num_products'],
                'Is Cheapest': platform == results['cheapest']['platform']
            })
        
        df = pd.DataFrame(df_data)
        df.to_csv('price_comparison_results.csv', index=False)
        print("\n结果已保存到 price_comparison_results.csv")