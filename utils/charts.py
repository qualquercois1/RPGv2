def get_hexagon_chart_html(f, a, i, v, s, m):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0; 
                padding: 0;
                /* Fundo transparente para mesclar com o container do Streamlit */
                background-color: transparent; 
                font-family: 'Inter', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }}
            canvas {{
                display: block;
                max-width: 100%;
            }}
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>

        <script>
            var canvas = document.getElementById('canvas');
            // Tamanho ajustado para caber bem no layout do Streamlit
            canvas.width = 500;
            canvas.height = 500; 

            var container = canvas.getContext("2d");
            var screen_width = canvas.width;
            var screen_height = canvas.height;
            // Raio ajustado para o novo tamanho do canvas
            var radius = 65; 

            function verticeAccountX(position, angle, radius) {{
                var radian = angle * (Math.PI / 180);
                return position + (radius * (Math.cos(radian)));
            }}

            function verticeAccountY(position, angle, radius) {{
                var radian = angle * (Math.PI / 180);
                return position + (radius * (Math.sin(radian)));
            }}

            function drawLine(v1x, v1y, v2x, v2y, color) {{
                container.strokeStyle = color;
                container.lineWidth = 2;
                container.beginPath();
                container.moveTo(v1x, v1y);
                container.lineTo(v2x, v2y);
                container.stroke();
            }}

            function makeHexagon(centerX, centerY, radius, color) {{
                var vertice_x = verticeAccountX(centerX, 0, radius);
                var vertice_y = verticeAccountY(centerY, 0, radius);
                var vertices = [{{x: vertice_x, y: vertice_y}}];
                
                for(var j=1; j<=6; j++) {{
                    var antigo_vertice_x = vertice_x;
                    var antigo_vertice_y = vertice_y;
                    vertice_x = verticeAccountX(centerX, j*60, radius);
                    vertice_y = verticeAccountY(centerY, j*60, radius);
                    drawLine(antigo_vertice_x, antigo_vertice_y, vertice_x, vertice_y, color);
                    vertices.push({{ x: vertice_x, y: vertice_y }});
                }}
                return vertices;
            }}

            function lerp(start, end, value) {{
                // Assumindo que o valor máximo do atributo é 100 para calcular a porcentagem
                var t = value / 100.0;
                if (t < 0) t = 0;
                if (t > 1) t = 1; 
                return start + (end - start) * t;
            }}

            function meter(forca, agilidade, inteligencia, vitalidade, sobrevivencia, magia) {{
                var vertices_internal = null;
                var vertices_external = null;
                var attributes = [forca, agilidade, inteligencia, vitalidade, sobrevivencia, magia];
                var attributeNames = ["FOR", "AGI", "INT", "VIT", "SOB", "MAG"];

                for(var j=1; j<=3; j++) {{
                    // Cor das teias de fundo (ajustada para ficar sutil)
                    var tempVertices = makeHexagon(screen_width/2, screen_height/2, radius*j, "rgba(255, 115, 0, 0.3)");
                    if(j == 1) {{ vertices_internal = tempVertices; }} 
                    else if (j == 3) {{ vertices_external = tempVertices; }}
                }}

                for(var j=0; j<6; j++) {{
                    var end_point_x = vertices_external[j].x;
                    var end_point_y = vertices_external[j].y;
                    var textX = end_point_x;
                    var textY = end_point_y;
                    var nameLabel = attributeNames[j]; 
                    var valueLabel = attributes[j];

                    container.fillStyle = "#ffffff"; 
                    container.font = "bold 16px Inter, sans-serif";
                    
                    if (j === 0 || j === 1 || j === 5) {{
                        container.textAlign = "left";
                        textX += 15; 
                    }} else {{
                        container.textAlign = "right";
                        textX -= 15;
                    }}
                    
                    var gap = 4;
                    container.textBaseline = "bottom"; 
                    container.fillText(nameLabel, textX, textY - gap);
                    
                    container.fillStyle = "#bbff00";
                    container.textBaseline = "top"; 
                    container.fillText(valueLabel, textX, textY + gap);
                }}

                var attributeVertices = [];
                for (var j = 0; j < 6; j++) {{
                    var startX = vertices_internal[j].x;
                    var startY = vertices_internal[j].y;
                    var endX = vertices_external[j].x;
                    var endY = vertices_external[j].y;
                    
                    var attrValue = attributes[j];
                    var pointX = lerp(startX, endX, attrValue);
                    var pointY = lerp(startY, endY, attrValue);
                    attributeVertices.push({{ x: pointX, y: pointY }});
                }}

                container.beginPath();
                container.moveTo(attributeVertices[0].x, attributeVertices[0].y);
                for (var j = 1; j < 6; j++) {{
                    container.lineTo(attributeVertices[j].x, attributeVertices[j].y);
                }}
                container.lineTo(attributeVertices[0].x, attributeVertices[0].y); 
                
                // Cor da linha principal
                container.strokeStyle = "#bbff00";
                container.lineWidth = 3;
                container.stroke();
                
                // Preenchimento interno
                container.fillStyle = "rgba(200, 255, 0, 0.4)";
                container.fill();
            }}

            // INJEÇÃO DE DADOS (Substitui as variáveis f-string do Python)
            meter({f}, {a}, {i}, {v}, {s}, {m});
            
        </script>
    </body>
    </html>
    """

def get_attributes_html(f,a,i,v,s,m):
    return f"""
            <style>
                .attr-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .attr-box {{
                    background-color: #2b2d35;
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid #444;
                }}
                .attr-val {{
                    font-size: 1.8em;
                    font-weight: bold;
                    color: #fff;
                }}
                .attr-label {{
                    font-size: 0.8em;
                    color: #aaa;
                    margin-top: 5px;
                }}
            </style>
            
            <div class="attr-grid">
                <div class="attr-box"><div class="attr-val">{f}</div><div class="attr-label">FORÇA</div></div>
                <div class="attr-box"><div class="attr-val">{a}</div><div class="attr-label">AGILIDADE</div></div>
                <div class="attr-box"><div class="attr-val">{v}</div><div class="attr-label">VITALIDADE</div></div>
                <div class="attr-box"><div class="attr-val">{i}</div><div class="attr-label">INTELIGÊNCIA</div></div>
                <div class="attr-box"><div class="attr-val">{s}</div><div class="attr-label">SOBREVIVÊNCIA</div></div>
                <div class="attr-box"><div class="attr-val">{m}</div><div class="attr-label">MAGIA</div></div>
            </div>
            """