---
title: ""
date: 2025-05-15
draft: false
---

<div id="curriculo" style="max-width: 900px; margin: auto; padding: 1rem;">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div>
      <strong style="font-size: 1.2rem;">Felipe da Matta</strong><br>
      <em>Cloud Architect | DevOps SRE</em><br>
      São Paulo, Brasil<br>
      <a href="https://www.linkedin.com/in/fmatta1/">LinkedIn</a> • 
      <a href="https://github.com/fxshelll">GitHub</a> • 
      <a href="mailto:feededamatta@gmail.com">E-mail</a>
    </div>
    <img src="/fx.png" alt="Foto" style="height: 100px; border-radius: 12px;">
  </div>

  <hr>

  <h3>🧠 Resumo</h3>
  <p>Sou formado em Defesa Cibernética e atualmente atuo como DevOps/SRE, com foco em ambientes resilientes, escaláveis e seguros. Gosto de criar laboratórios, testar ferramentas e documentar tudo como forma de compartilhar conhecimento. Busco sempre entregar soluções seguras, inteligentes e sem enrolação.</p>

---

  <h3>🚀 Especialidades</h3>
  <ul>
    <li><strong>Cloud & Infraestrutura:</strong> AWS, Azure — administração de ambientes Windows e Linux, provisionamento e gerenciamento completo de infraestrutura em nuvem.</li>
    <li><strong>Infrastructure as Code (IaC):</strong> Terraform, Ansible, Chef.</li>
    <li><strong>Contêineres & Orquestração:</strong> Kubernetes (EKS e AKS), Helm Charts.</li>
    <li><strong>CI/CD & Automação:</strong> GitHub Actions, Jenkins, ArgoCD, Azure DevOps, FluxCD.</li>
    <li><strong>Servidores Web & HTTPS:</strong> NGINX, IIS, Apache.</li>
    <li><strong>Scripting & Programação:</strong> Bash, PowerShell, Python, Go.</li>
    <li><strong>Observabilidade & Alertas:</strong> Elasticsearch, Grafana, Prometheus, Zabbix, CloudWatch, Opsgenie.</li>
    <li><strong>Segurança e Gestão de Segredos:</strong> Vault by HashiCorp, API Gateway, Ingress Controller.</li>
    <li><strong>Performance & Distribuição de Conteúdo:</strong> Akamai, CloudFront.</li>
    <li><strong>Bancos de Dados:</strong> MySQL, MongoDB.</li>
    <li><strong>Documentação e Organização de Times:</strong> Confluence, Jira, Sharepoint.</li>
  </ul>

---

  <h3>💼 Experiência</h3>
  
<strong>Grupo NC — DevOps Sênior</strong>  
 <em>Fev 2025 – Atual</em>
  <ul>
    <li>Gestão de infraestrutura em nuvem com AWS</li>
    <li>Administração de clusters Kubernetes (AKS)</li>
    <li>Automatizações com Terraform, Shellscript, PowerShell</li>
    <li>GitOps com ArgoCD e CI/CD com GitHub Actions</li>
    <li>Observabilidade com DataDog</li>
    <li>HashiCorp Vault para segredos e autenticação</li>
    <li>Confluence e Jira para documentação</li>
  </ul>

---

<strong>Linx — DevOps Sênior / Pleno</strong>  
 <em>Abr 2021 – Jan 2025</em>

  <ul>
    <li>Infraestrutura em nuvem com AZURE</li>
    <li>Kubernetes (EKS), Let's Encrypt, Jenkins, GitHub</li>
    <li>Ansible e AWX, Terraform</li>
    <li>Integrações com Azure DevOps</li>
    <li>Webservers Linux e Windows</li>
  </ul>

---

<strong>Portal R7 — Admin. de Sistemas / Suporte TI</strong>  
 <em>2017 – 2021</em>

  <ul>
    <li>Ambientes em AWS, suporte a CMS e blogs</li>
    <li>Monitoramento com Zabbix</li>
    <li>Atendimento técnico com OTRS</li>
  </ul>

---

  <h3>🎓 Formação e Certificações</h3>
  <ul>
    <li>FIAP — Defesa Cibernética (2018–2020)</li>
    <li>RH124 – Red Hat Academy (2021)</li>
    <li>LinuxTips – Docker (2021)</li>
    <li>FIAP – Perícia Forense, Ethical Hacking (2020)</li>
  </ul>

---

  <h3>🏆 Destaques</h3>
  <ul>
    <li>🏅 Finalista do Innovation Challenge Itaú-FIAP 2020</li>
    <li>🤝 Participação ativa em squads DevSecOps</li>
  </ul>
</div>

<!-- Botão -->
<div style="text-align: right; margin-top: 20px;">
  <button onclick="gerarPDF()" style="
    background-color: #ff69b4;
    color: black;
    border: none;
    padding: 10px 16px;
    font-weight: bold;
    border-radius: 8px;
    font-family: monospace;
    cursor: pointer;
  ">
    📄 Baixar Currículo em PDF
  </button>
</div>

<!-- Lib html2pdf -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

<!-- Script PDF -->
<script>
function gerarPDF() {
  const original = document.getElementById('curriculo');
  const clone = original.cloneNode(true);

  // Criar o wrapper que envolve o currículo
  const wrapper = document.createElement('div');
  wrapper.style.backgroundColor = '#000000';
  wrapper.style.color = '#ffffff';
  wrapper.style.padding = '20px';
  wrapper.style.fontFamily = 'monospace';
  wrapper.style.boxSizing = 'border-box';
  wrapper.style.width = '210mm';
  wrapper.style.height = '590mm'; // ligeiramente menor que 594mm
  wrapper.style.overflow = 'hidden';
  wrapper.style.position = 'relative';

  // Filler pra manter fundo preto até o fim


---

## 📎 Contato

- [LinkedIn](https://www.linkedin.com/in/fmatta)
- [GitHub](https://github.com/fxshelll)
- [E-mail](mailto:felipepmatta@gmail.com)
