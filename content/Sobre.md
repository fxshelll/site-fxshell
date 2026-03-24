---
title: ""
date: 2025-05-15
draft: false
---

<style>
  #curriculo {
    max-width: 860px;
    margin: auto;
    padding: 1.5rem;
    font-family: 'Courier New', monospace;
    color: #e0e0e0;
  }

  #curriculo h3 {
    color: #ff69b4;
    border-bottom: 1px solid #333;
    padding-bottom: 4px;
    margin-top: 1.6rem;
  }

  .cv-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .cv-header-info h2 {
    margin: 0 0 2px 0;
    font-size: 1.4rem;
    color: #ffffff;
  }

  .cv-header-info .cv-role {
    color: #ff69b4;
    font-size: 0.95rem;
    margin-bottom: 6px;
  }

  .cv-header-info .cv-location {
    font-size: 0.85rem;
    color: #999;
  }

  .cv-links {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 8px;
  }

  .cv-links a {
    color: #ff69b4;
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid #ff69b4;
    padding: 2px 8px;
    border-radius: 4px;
    transition: background 0.2s;
  }

  .cv-links a:hover {
    background: #ff69b422;
  }

  .cv-photo {
    height: 90px;
    border-radius: 10px;
    border: 2px solid #ff69b4;
  }

  /* Skill badges */
  .skill-group {
    margin-bottom: 10px;
  }

  .skill-group-label {
    font-size: 0.78rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
  }

  .skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .skill-tag {
    background: #1a1a1a;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 2px 9px;
    font-size: 0.8rem;
    font-family: monospace;
  }

  /* Timeline */
  .job {
    margin-bottom: 1.4rem;
    padding-left: 14px;
    border-left: 2px solid #ff69b455;
  }

  .job-header {
    margin-bottom: 4px;
  }

  .job-title {
    font-weight: bold;
    color: #ffffff;
    font-size: 0.95rem;
  }

  .job-company {
    color: #ff69b4;
    font-size: 0.88rem;
  }

  .job-period {
    font-size: 0.78rem;
    color: #888;
    margin-top: 2px;
  }

  .job ul {
    margin: 6px 0 0 0;
    padding-left: 18px;
  }

  .job ul li {
    font-size: 0.85rem;
    color: #ccc;
    margin-bottom: 3px;
  }

  /* Edu & certs */
  .edu-item {
    margin-bottom: 6px;
    font-size: 0.88rem;
  }

  .edu-item strong {
    color: #e0e0e0;
  }

  .edu-item span {
    color: #888;
    font-size: 0.8rem;
  }

  /* Languages */
  .lang-grid {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .lang-item {
    background: #1a1a1a;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 0.85rem;
  }

  .lang-item span {
    display: block;
    font-size: 0.72rem;
    color: #888;
    margin-top: 2px;
  }

  /* Destaques */
  .highlight-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    font-size: 0.88rem;
  }

  /* Divider */
  .cv-divider {
    border: none;
    border-top: 1px solid #2a2a2a;
    margin: 1.2rem 0;
  }

  /* Botão PDF */
  #btn-pdf {
    background: transparent;
    color: #ff69b4;
    border: 1px solid #ff69b4;
    padding: 8px 18px;
    font-weight: bold;
    border-radius: 6px;
    font-family: monospace;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  #btn-pdf:hover {
    background: #ff69b4;
    color: #000;
  }

  #btn-pdf:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>

<div id="curriculo">

  <!-- HEADER -->
  <div class="cv-header">
    <div class="cv-header-info">
      <h2>Felipe da Matta</h2>
      <div class="cv-role">Cloud Architect · DevOps SRE</div>
      <div class="cv-location">📍 São Paulo, Brasil</div>
      <div class="cv-links">
        <a href="https://www.linkedin.com/in/fmatta/" target="_blank">LinkedIn</a>
        <a href="https://github.com/fxshelll" target="_blank">GitHub</a>
        <a href="mailto:felipepmatta@gmail.com">E-mail</a>
      </div>
    </div>
    <img src="/fx.png" alt="Felipe da Matta" class="cv-photo">
  </div>

  <hr class="cv-divider">

  <!-- RESUMO -->
  <h3>▸ Resumo</h3>
  <p style="font-size:0.88rem; color:#ccc; line-height:1.7;">
    Profissional com formação em Defesa Cibernética e pós-graduação em andamento em DevOps &amp; Arquitetura Cloud (FIAP).
    Atuo como DevOps/SRE entregando ambientes resilientes, escaláveis e seguros, com foco em automação, observabilidade
    e práticas DevSecOps. Tenho experiência em ambientes de missão crítica e alta disponibilidade, atuando tanto em
    AWS quanto Azure. Apaixonado por CTFs, laboratórios e por documentar o que aprendo.
  </p>

  <hr class="cv-divider">

  <!-- SKILLS -->
  <h3>▸ Stack Técnica</h3>

  <div class="skill-group">
    <div class="skill-group-label">Cloud & Infra</div>
    <div class="skill-tags">
      <span class="skill-tag">AWS</span>
      <span class="skill-tag">Azure</span>
      <span class="skill-tag">Linux</span>
      <span class="skill-tag">Windows Server</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">IaC & Automação</div>
    <div class="skill-tags">
      <span class="skill-tag">Terraform</span>
      <span class="skill-tag">Ansible / AWX</span>
      <span class="skill-tag">Chef</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">Contêineres & Orquestração</div>
    <div class="skill-tags">
      <span class="skill-tag">Kubernetes (EKS / AKS)</span>
      <span class="skill-tag">Docker</span>
      <span class="skill-tag">Helm</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">CI/CD & GitOps</div>
    <div class="skill-tags">
      <span class="skill-tag">GitHub Actions</span>
      <span class="skill-tag">ArgoCD</span>
      <span class="skill-tag">FluxCD</span>
      <span class="skill-tag">Jenkins</span>
      <span class="skill-tag">Azure DevOps</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">Observabilidade</div>
    <div class="skill-tags">
      <span class="skill-tag">Grafana</span>
      <span class="skill-tag">Prometheus</span>
      <span class="skill-tag">Elasticsearch / Kibana</span>
      <span class="skill-tag">Zabbix</span>
      <span class="skill-tag">Datadog</span>
      <span class="skill-tag">CloudWatch</span>
      <span class="skill-tag">Opsgenie</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">Segurança & Secrets</div>
    <div class="skill-tags">
      <span class="skill-tag">HashiCorp Vault</span>
      <span class="skill-tag">API Gateway</span>
      <span class="skill-tag">Ingress Controller</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">Scripting & Dev</div>
    <div class="skill-tags">
      <span class="skill-tag">Bash</span>
      <span class="skill-tag">PowerShell</span>
      <span class="skill-tag">Python</span>
      <span class="skill-tag">Go</span>
    </div>
  </div>

  <div class="skill-group">
    <div class="skill-group-label">Web & CDN</div>
    <div class="skill-tags">
      <span class="skill-tag">NGINX</span>
      <span class="skill-tag">Apache</span>
      <span class="skill-tag">IIS</span>
      <span class="skill-tag">Akamai</span>
      <span class="skill-tag">CloudFront</span>
      <span class="skill-tag">Varnish</span>
    </div>
  </div>

  <hr class="cv-divider">

  <!-- EXPERIÊNCIA -->
  <h3>▸ Experiência</h3>

  <div class="job">
    <div class="job-header">
      <div class="job-title">DevOps SRE</div>
      <div class="job-company">Sinqia — alocado na B3 (Bolsa de Valores)</div>
      <div class="job-period">Set 2025 – Atual</div>
    </div>
    <ul>
      <li>Ambiente de missão crítica e alta disponibilidade na B3</li>
      <li>Gerenciamento e otimização de infraestrutura no Microsoft Azure</li>
      <li>Pipelines CI/CD com GitHub Actions; versionamento de DB com Flyway</li>
      <li>Provisionamento com Azure CLI, Terraform e Ansible/AWX</li>
      <li>Administração de workloads no AKS (deploys, troubleshooting, manifests YAML)</li>
      <li>Monitoramento com Grafana; consultas SQL e suporte às esteiras de deploy</li>
      <li>Testes e integração com APIs via Postman</li>
    </ul>
  </div>

  <div class="job">
    <div class="job-header">
      <div class="job-title">DevOps Sênior (PJ)</div>
      <div class="job-company">Grupo NC</div>
      <div class="job-period">Fev 2025 – Set 2025</div>
    </div>
    <ul>
      <li>Gestão de infraestrutura AWS com foco em resiliência e escalabilidade</li>
      <li>Administração de clusters EKS (deploys, upgrades, gestão de recursos)</li>
      <li>Automação com Terraform, Shell Script e PowerShell</li>
      <li>GitOps com ArgoCD e pipelines CI/CD no GitHub Actions</li>
      <li>Observabilidade com Datadog; gerenciamento de segredos com HashiCorp Vault</li>
    </ul>
  </div>

  <div class="job">
    <div class="job-header">
      <div class="job-title">DevOps Sênior / Pleno</div>
      <div class="job-company">Linx</div>
      <div class="job-period">Abr 2021 – Jan 2025</div>
    </div>
    <ul>
      <li>Provisionamento e gestão de infra Azure (alta disponibilidade)</li>
      <li>Orquestração com Kubernetes AKS (deploys, ingress, workloads)</li>
      <li>NGINX, reverse proxy e balanceamento de carga em produção</li>
      <li>Automação com Terraform, Ansible e AWX</li>
      <li>Pipelines com Jenkins, GitHub e Azure DevOps</li>
      <li>TLS com Let's Encrypt; administração do Apache Solr em e-commerce</li>
    </ul>
  </div>

  <div class="job">
    <div class="job-header">
      <div class="job-title">Administrador de Sistemas / Suporte TI</div>
      <div class="job-company">Portal R7</div>
      <div class="job-period">2017 – 2021</div>
    </div>
    <ul>
      <li>Administração de ambientes AWS em plataforma de alta audiência</li>
      <li>Sustentação do CMS proprietário do R7 (artigos, vídeos, widgets)</li>
      <li>Cache reverso com Varnish; monitoramento com Zabbix; logs com Kibana</li>
      <li>Troubleshooting de servidores Linux; gestão de chamados via OTRS</li>
    </ul>
  </div>

  <hr class="cv-divider">

  <!-- FORMAÇÃO -->
  <h3>▸ Formação & Certificações</h3>

  <div class="edu-item">
    <strong>FIAP</strong> — Graduação em Defesa Cibernética
    <span>· 2018 – 2020</span>
  </div>
  <div class="edu-item">
    <strong>FIAP</strong> — Pós-Tech em DevOps e Arquitetura Cloud
    <span>· 2025 – em andamento</span>
  </div>
  <div class="edu-item">
    <strong>Red Hat Academy</strong> — RH124
    <span>· 2021</span>
  </div>
  <div class="edu-item">
    <strong>LinuxTips</strong> — Docker
    <span>· 2021</span>
  </div>
  <div class="edu-item">
    <strong>FIAP</strong> — Perícia Forense &amp; Ethical Hacking
    <span>· 2020</span>
  </div>

  <hr class="cv-divider">

  <!-- IDIOMAS -->
  <h3>▸ Idiomas</h3>
  <div class="lang-grid">
    <div class="lang-item">
      🇧🇷 Português
      <span>Nativo</span>
    </div>
    <div class="lang-item">
      🇺🇸 Inglês
      <span>Intermediário / Técnico</span>
    </div>
  </div>

  <hr class="cv-divider">

  <!-- DESTAQUES -->
  <h3>▸ Destaques</h3>
  <div class="highlight-item">🏅 Finalista — Innovation Challenge Itaú-FIAP 2020</div>
  <div class="highlight-item">🛡️ Participação ativa em squads DevSecOps</div>
  <div class="highlight-item">🔐 Estudo contínuo em CTFs e laboratórios de segurança ofensiva (HTB)</div>

</div>

<!-- Botão PDF -->
<div style="text-align: right; margin-top: 1.5rem; margin-bottom: 1rem;">
  <button id="btn-pdf" onclick="gerarPDF()">
    <span id="btn-icon">📄</span> Baixar PDF
  </button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
  function gerarPDF() {
    const btn = document.getElementById('btn-pdf');
    btn.disabled = true;
    btn.innerHTML = '⏳ Gerando...';

    const original = document.getElementById('curriculo');
    const clone = original.cloneNode(true);

    // Estilos específicos para o PDF — sem sobrescrever backgrounds globais
    const style = document.createElement('style');
    style.textContent = `
      #cv-pdf-wrapper {
        background-color: #000000 !important;
      }
      #cv-pdf-wrapper * {
        color: #ffffff !important;
        font-size: 0.88em !important;
        line-height: 1.45 !important;
      }
      #cv-pdf-wrapper h2 {
        color: #ffffff !important;
        font-size: 1.3em !important;
        margin-bottom: 2px !important;
      }
      #cv-pdf-wrapper h3 {
        color: #ff69b4 !important;
        font-size: 1.0em !important;
        border-bottom: 1px solid #333 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.4rem !important;
      }
      #cv-pdf-wrapper .cv-role {
        color: #ff69b4 !important;
      }
      #cv-pdf-wrapper .job-title {
        color: #ffffff !important;
        font-size: 1.05em !important;
      }
      #cv-pdf-wrapper .job-company {
        color: #ff69b4 !important;
      }
      #cv-pdf-wrapper .job-period,
      #cv-pdf-wrapper .cv-location,
      #cv-pdf-wrapper .edu-item span,
      #cv-pdf-wrapper .lang-item span,
      #cv-pdf-wrapper .skill-group-label {
        color: #aaaaaa !important;
      }
      #cv-pdf-wrapper a {
        color: #ff69b4 !important;
        text-decoration: none !important;
        border-color: #ff69b4 !important;
      }
      #cv-pdf-wrapper .skill-tag {
        background-color: #1a1a1a !important;
        border: 1px solid #555 !important;
        color: #ffffff !important;
      }
      #cv-pdf-wrapper .lang-item {
        background-color: #1a1a1a !important;
        border: 1px solid #555 !important;
      }
      #cv-pdf-wrapper .job {
        border-left: 2px solid #ff69b4 !important;
        margin-bottom: 0.6rem !important;
        padding-left: 10px !important;
      }
      #cv-pdf-wrapper .cv-divider {
        margin: 0.5rem 0 !important;
      }
      #cv-pdf-wrapper .skill-group {
        margin-bottom: 5px !important;
      }
      #cv-pdf-wrapper ul {
        margin: 3px 0 0 0 !important;
        padding-left: 14px !important;
      }
      #cv-pdf-wrapper ul li {
        margin-bottom: 1px !important;
      }
      #cv-pdf-wrapper .cv-divider {
        border-top: 1px solid #333 !important;
        background: transparent !important;
      }
      #cv-pdf-wrapper ul li {
        color: #ffffff !important;
      }
      #cv-pdf-wrapper p {
        color: #ffffff !important;
      }
    `;
    clone.id = 'cv-pdf-clone';

    const wrapper = document.createElement('div');
    wrapper.id = 'cv-pdf-wrapper';
    wrapper.style.cssText = `
      background-color: #000000;
      color: #ffffff;
      padding: 14px 24px;
      font-family: 'Courier New', monospace;
      font-size: 13px;
      width: 794px;
      box-sizing: border-box;
    `;
    wrapper.appendChild(style);
    wrapper.appendChild(clone);

    const container = document.createElement('div');
    // SEM visibility:hidden — html2canvas não renderiza elementos ocultos
    container.style.cssText = 'position:fixed;top:-9999px;left:-9999px;';
    container.appendChild(wrapper);
    document.body.appendChild(container);

    html2canvas(wrapper, {
      scale: 2,
      backgroundColor: '#000000',
      useCORS: true,
      scrollY: 0,
      windowWidth: 794
    }).then(canvas => {
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF({ unit: 'mm', format: 'a4', orientation: 'portrait' });

      const pageW = pdf.internal.pageSize.getWidth();
      const pageH = pdf.internal.pageSize.getHeight();
      const pxPerMm  = canvas.width / pageW;
      const pageHpx  = pageH * pxPerMm;
      const total    = Math.ceil(canvas.height / pageHpx);

      for (let p = 0; p < total; p++) {
        if (p > 0) pdf.addPage();

        // Fundo preto garantido via jsPDF também
        pdf.setFillColor(0, 0, 0);
        pdf.rect(0, 0, pageW, pageH, 'F');

        // Canvas da página: preto + fatia do conteúdo por cima
        const pc = document.createElement('canvas');
        pc.width  = canvas.width;
        pc.height = Math.round(pageHpx);
        const ctx = pc.getContext('2d');
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, pc.width, pc.height);

        const srcY = Math.round(p * pageHpx);
        const srcH = Math.min(Math.round(pageHpx), canvas.height - srcY);
        if (srcH > 0) {
          ctx.drawImage(canvas, 0, srcY, canvas.width, srcH, 0, 0, canvas.width, srcH);
        }

        pdf.addImage(pc.toDataURL('image/jpeg', 0.98), 'JPEG', 0, 0, pageW, pageH);
      }

      pdf.save('curriculo-felipe-da-matta.pdf');
      document.body.removeChild(container);
      btn.disabled = false;
      btn.innerHTML = '📄 Baixar PDF';
    }).catch(err => {
      console.error('Erro ao gerar PDF:', err);
      document.body.removeChild(container);
      btn.disabled = false;
      btn.innerHTML = '📄 Baixar PDF';
    });
  }
</script>
