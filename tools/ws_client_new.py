import asyncio
import json
from datetime import datetime
import websockets
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def create_status_table(status_data):
    """建立顯示震度資訊的表格"""
    table = Table(title="TREM-Lite 即時震度監測")
    table.add_column("地區", style="cyan")
    table.add_column("震度", style="magenta")
    table.add_column("PGA (gal)", style="yellow")
    table.add_column("最後更新", style="green")

    for area_code, data in status_data.items():
        # 根據震度選擇顏色
        intensity_style = "white"
        if data["intensity"] >= 7:
            intensity_style = "red"
        elif data["intensity"] >= 5:
            intensity_style = "yellow"
        elif data["intensity"] >= 3:
            intensity_style = "green"
        elif data["intensity"] >= 1:
            intensity_style = "blue"

        table.add_row(
            data["name"],
            f"[{intensity_style}]{data['intensityText']}[/]",
            f"{data['pga']:.2f}",
            data["lastUpdate"] if data["lastUpdate"] else "尚無資料"
        )
    
    return table

async def connect_websocket():
    """連接到 WebSocket 服務器並處理資料"""
    uri = "ws://localhost:3000"
    status_data = {}  # 儲存最新狀態
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                console.print(f"[green]成功連接到 TREM-Lite 服務器[/green]")
                
                with Live(create_status_table(status_data), auto_refresh=True) as live:
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        if data["type"] == "status":
                            status_data = data["data"]  # 更新狀態資料
                            table = create_status_table(status_data)
                            live.update(table)
                            
        except websockets.exceptions.ConnectionClosed:
            console.print("[yellow]連接已關閉，嘗試重新連接...[/yellow]")
            await asyncio.sleep(1)
        except Exception as e:
            console.print(f"[red]發生錯誤: {str(e)}[/red]")
            await asyncio.sleep(1)

if __name__ == "__main__":
    console.print("[cyan]啟動 TREM-Lite 監測客戶端...[/cyan]")
    console.print("按 Ctrl+C 結束程式\n")
    
    try:
        asyncio.run(connect_websocket())
    except KeyboardInterrupt:
        console.print("\n[yellow]程式已結束[/yellow]")