var viz;
entity = $("#entity")
find = $("#find")
info = $("#info")
header = $("#header")
list = $("#list")
close = $("#collapse")
var sidebar = $(".col-3");
// 在页面加载完成后执行
$(document).ready(function () {
    // 初始隐藏侧边栏
    sidebar.hide();
});

function draw() {
    var config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "yan011017",
        },
        labels: {
            Person: {
                label: "name",
            },
            Movie: {
                label: "title",
            },
            Genre: {
                label: "name",
            },
        },
        visConfig: {
            edges: {
                arrow: {
                    to: {
                        enabled: true,
                    }
                }
            }
        },
        initialCypher:
            "MATCH (n)-[r:actedin]->(m)-[r2:is]->(g) RETURN * LIMIT 100",
    };

    viz = new NeoVis.default(config);
    viz.render();
    // 使用registerOnEvent方法来处理点击节点事件
    viz.registerOnEvent("clickNode", function (node) {
        console.log(node);
        var label = node.node.label;
        var properties = node.node.raw.properties;
        console.log(properties);
        header.text(label);
        var html = "";
        for (var key in properties) {
            if (key === "rating") {
                html += `<li class="list-group-item">评分:${properties[key]}</li>`;
            }
            if (key === "releasedate") {
                html += `<li class="list-group-item">上映日期:${properties[key]}</li>`;
            }
            if (key === "introduction") {
                html += `<li class="list-group-item">简介:${properties[key]}</li>`;
            }
            if (key === "bio") {
                if (properties[key] === "No biography available") {
                    html += `<li class="list-group-item">演员简介:暂无简介</li>`;
                } else
                    html += `<li class="list-group-item">演员简介:${properties[key]}</li>`;
            }
            if (key === "gid") {
                html += `<li class="list-group-item">标签编号:${properties[key]}</li>`;
            }
        }
        if ("url" in properties) {
            html += `<li class="list-group-item list-group-flush"><a class="btn btn-outline-dark" href="${properties[key]}">点击跳转源网页</a></li>`;
        }
        list.html(html);
        sidebar.show();
    });
    // 在点击节点以外的地方隐藏侧边栏
    $(document).on("click", function (event) {
        if (!$(event.target).closest(".col-3").length && !$(event.target).closest("#viz").length) {
            sidebar.hide();
        }
    });

}

//点击查询
find.click(function () {
    var text = entity.val();
    var cypher = "MATCH (n:Person)-[r:actedin]->(m:Movie)-[r2:is]->(g:Genre) WHERE m.title contains '" + text + "' or n.name contains '" + text + "' RETURN * LIMIT 10";
    if (text.length > 0) {
        viz.renderWithCypher(cypher);
    } else {
        viz.reload();
    }
    entity.val("");
})
// 按回车触发查询
$('body').keydown(function (e) {
    if (e.keyCode === 13) {
        find.click();
    }
})
//隐藏侧边栏
close.click(function () {
    sidebar.hide()
})