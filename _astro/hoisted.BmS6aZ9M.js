async function a(){try{const e=new Date().getTime(),s=await(await fetch(`/data/buy-plan.json?t=${e}`,{cache:"no-cache"})).json();d(s)}catch(e){console.error("加载失败:",e),document.getElementById("no-data").classList.remove("hidden")}}function d(e){document.getElementById("update-time").textContent=e.updateTime,document.getElementById("market-status").textContent=e.marketStatus,document.getElementById("position-advice").textContent=e.positionAdvice,document.getElementById("stock-count").textContent=e.count;const t=document.getElementById("stock-list");if(e.count===0){document.getElementById("no-data").classList.remove("hidden");return}e.stocks.forEach(s=>{const n=i(s);t.appendChild(n)})}function i(e){const t=document.createElement("div");t.className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow";const s=e.recommendation?.includes("🔥")?"🔥":e.recommendation?.includes("⭕")?"⭕":"⚪",n=e.recommendation?.includes("🔥")?"bg-red-100 text-red-800":e.recommendation?.includes("⭕")?"bg-green-100 text-green-800":"bg-gray-100 text-gray-800";return t.innerHTML=`
                <div class="p-6">
                    <!-- 标题 -->
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">${e.code} ${e.name}</h3>
                            <p class="text-sm text-gray-500">现价：¥${e.currentPrice?.toFixed(2)}</p>
                        </div>
                        <span class="px-3 py-1 rounded-full text-sm font-medium ${n}">
                            ${s}
                        </span>
                    </div>

                    <!-- 买入类型 -->
                    <div class="mb-4">
                        <span class="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                            ${e.buyType}
                        </span>
                    </div>

                    <!-- 核心数据 -->
                    <div class="space-y-3 mb-4">
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">推荐买入价</span>
                            <span class="font-bold text-green-600">¥${e.buyPrice?.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">可接受区间</span>
                            <span class="text-gray-800 text-sm">${e.buyRange}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">止损位</span>
                            <span class="font-bold text-red-600">¥${e.stopLoss?.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">止损距离</span>
                            <span class="text-gray-800 text-sm">${e.stopDistance?.toFixed(1)}%</span>
                        </div>
                    </div>

                    <!-- 仓位信息 -->
                    <div class="border-t pt-3 mb-4">
                        <div class="flex justify-between mb-2">
                            <span class="text-gray-600 text-sm">建议股数</span>
                            <span class="font-medium text-gray-800">${e.shares?.toLocaleString()}股</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">总金额</span>
                            <span class="font-medium text-gray-800">¥${e.value?.toLocaleString()}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 text-sm">占仓位</span>
                            <span class="font-medium text-gray-800">${e.positionPercent?.toFixed(1)}%</span>
                        </div>
                    </div>

                    <!-- 催化剂 -->
                    <div class="border-t pt-3">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-gray-600 text-sm">催化剂评分</span>
                            <span class="font-bold ${e.catalystScore>=6?"text-red-600":e.catalystScore>=3?"text-green-600":"text-gray-600"}">
                                ${e.catalystScore}分
                            </span>
                        </div>
                        ${e.warning?`<p class="text-xs text-yellow-600 mt-1">⚠️ ${e.warning}</p>`:""}
                    </div>
                </div>

                <!-- 底部操作提示 -->
                <div class="bg-gray-50 px-6 py-3">
                    <p class="text-xs text-gray-500">
                        ⏰ 决策时间：14:30-15:00 | 📝 限价单执行
                    </p>
                </div>
            `,t}a();setInterval(a,5*60*1e3);
