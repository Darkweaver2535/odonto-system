/**
 * odontograma.js - Script compartido para funcionalidad del odontograma
 * Este archivo contiene todas las funciones necesarias para renderizar y 
 * manipular el odontograma en las diferentes vistas (crear, editar, detalles)
 */

// Configuración del odontograma
const dentitionConfig = {
    'permanente': {
        'upper-right': [18, 17, 16, 15, 14, 13, 12, 11],
        'upper-left': [21, 22, 23, 24, 25, 26, 27, 28],
        'lower-left': [31, 32, 33, 34, 35, 36, 37, 38],
        'lower-right': [48, 47, 46, 45, 44, 43, 42, 41]
    },
    'temporal': {
        'upper-right': [55, 54, 53, 52, 51],
        'upper-left': [61, 62, 63, 64, 65],
        'lower-left': [71, 72, 73, 74, 75],
        'lower-right': [85, 84, 83, 82, 81]
    },
    'mixta': {
        'upper-right': [18, 17, 16, 55, 54, 53, 52, 51],
        'upper-left': [61, 62, 63, 64, 65, 26, 27, 28],
        'lower-left': [71, 72, 73, 74, 75, 36, 37, 38],
        'lower-right': [48, 47, 46, 85, 84, 83, 82, 81]
    }
};

// Nombres en español para superficies y estados dentales
const surfaceNames = {
    'occlusal': 'Oclusal',
    'buccal': 'Bucal/Vestibular',
    'lingual': 'Lingual/Palatina',
    'mesial': 'Mesial',
    'distal': 'Distal',
    'incisal': 'Incisal'
};

const toolNames = {
    'caries': 'Caries',
    'restoration': 'Restauración',
    'extraction': 'Extracción',
    'crown': 'Corona',
    'implant': 'Implante',
    'bridge': 'Puente',
    'root-canal': 'Endodoncia',
    'sealant': 'Sellante',
    'veneer': 'Carilla',
    'fracture': 'Fractura',
    'mobility': 'Movilidad',
    'missing': 'Ausente',
    'prosthesis': 'Prótesis removible'
};

// Función para obtener color según herramienta
function getToolColor(tool) {
    switch (tool) {
        case 'caries': return 'rgba(220, 53, 69, 0.7)';
        case 'restoration': return 'rgba(40, 167, 69, 0.7)';
        case 'extraction': return 'rgba(108, 117, 125, 0.7)';
        case 'crown': return 'rgba(23, 162, 184, 0.7)';
        case 'implant': return 'rgba(111, 66, 193, 0.7)';
        case 'bridge': return 'rgba(253, 126, 20, 0.7)';
        case 'root-canal': return 'rgba(255, 193, 7, 0.7)';
        case 'sealant': return 'rgba(32, 201, 151, 0.7)';
        case 'veneer': return 'rgba(13, 202, 240, 0.7)';
        case 'fracture': return 'rgba(220, 85, 18, 0.7)';
        case 'mobility': return 'rgba(255, 152, 0, 0.7)';
        default: return 'transparent';
    }
}

function getToolColorClass(tool) {
    switch (tool) {
        case 'caries': return 'danger';
        case 'restoration': return 'success';
        case 'extraction': return 'secondary';
        case 'crown': return 'info';
        case 'implant': return 'primary';
        case 'bridge': return 'warning';
        case 'root-canal': return 'warning';
        case 'sealant': return 'success';
        case 'veneer': return 'info';
        case 'fracture': return 'danger';
        case 'mobility': return 'warning';
        case 'erase': return 'dark';
        default: return 'primary';
    }
}

function getIconForIntervention(interventionType) {
    switch (interventionType) {
        case 'caries': return 'fa-bacteria';
        case 'restoration': return 'fa-square';
        case 'extraction': return 'fa-times-circle';
        case 'missing': return 'fa-minus-circle';
        case 'crown': return 'fa-crown';
        case 'implant': return 'fa-screwdriver';
        case 'bridge': return 'fa-grip-lines';
        case 'root-canal': return 'fa-radiation-alt';
        case 'sealant': return 'fa-shield-alt';
        case 'veneer': return 'fa-layer-group';
        case 'fracture': return 'fa-bolt';
        case 'mobility': return 'fa-arrows-alt-h';
        default: return 'fa-tooth';
    }
}

// Clase principal del Odontograma
class Odontograma {
    constructor(options) {
        this.containerId = options.containerId || 'odontogram-container';
        this.teethData = options.teethData || {};
        this.readOnly = options.readOnly || false;
        this.activeTool = options.activeTool || 'caries';
        this.selectedTooth = null;
        this.dentition = options.dentition || 'permanente';
        this.onStateChange = options.onStateChange || function() {};
        this.activeToolDisplay = document.getElementById(options.activeToolDisplayId || 'active-tool-display');
    }
    
    // Inicializa el odontograma
    init() {
        this.renderOdontogram(this.dentition);
        if (!this.readOnly) {
            this.setupEventListeners();
        }
        this.setupTooltips();
        
        if (this.activeToolDisplay) {
            this.updateActiveToolDisplay();
        }
    }
    
    // Actualiza la herramienta activa
    setActiveTool(tool) {
        this.activeTool = tool;
        if (this.activeToolDisplay) {
            this.updateActiveToolDisplay();
        }
    }
    
    // Actualiza el display de herramienta activa
    updateActiveToolDisplay() {
        if (!this.activeToolDisplay) return;
        
        this.activeToolDisplay.textContent = toolNames[this.activeTool] || this.activeTool;
        this.activeToolDisplay.className = `badge bg-${getToolColorClass(this.activeTool)}-subtle text-${getToolColorClass(this.activeTool)}`;
    }
    
    // Configura eventos para botones de herramientas
    setupEventListeners() {
        const toolButtons = document.querySelectorAll('.tool-button');
        toolButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Quitar activo de todos los botones
                toolButtons.forEach(btn => btn.classList.remove('active'));
                
                // Activar este botón
                button.classList.add('active');
                
                // Establecer herramienta activa
                this.setActiveTool(button.dataset.tool);
                
                // Si hay un diente seleccionado y es un clic en "borrar", aplicarlo automáticamente
                if (this.selectedTooth && this.activeTool === 'erase') {
                    this.applyTool(this.selectedTooth);
                }
            });
        });
    }
    
    // Configura tooltips Bootstrap
    setupTooltips() {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                container: 'body',
                html: true,
                boundary: 'window'
            });
        });
    }
    
    // Renderiza el odontograma
    renderOdontogram(dentition) {
        const config = dentitionConfig[dentition];
        
        for (const [quadrant, teeth] of Object.entries(config)) {
            const quadrantElement = document.getElementById(quadrant);
            if (!quadrantElement) continue;
            
            // CREAR UN CONTENEDOR PARA LOS DIENTES (sin tocar el label)
            let teethContainer = quadrantElement.querySelector('.teeth-container');
            if (!teethContainer) {
                teethContainer = document.createElement('div');
                teethContainer.className = 'teeth-container';
                teethContainer.style.display = 'flex';
                
                // Preservar el label si existe o crearlo si no existe
                let labelElement = quadrantElement.querySelector('.arch-label');
                if (!labelElement) {
                    labelElement = document.createElement('div');
                    labelElement.className = 'arch-label';
                    
                    // Asignar el texto correcto según el cuadrante
                    if (quadrant === 'upper-right') labelElement.textContent = 'Superior Derecho';
                    else if (quadrant === 'upper-left') labelElement.textContent = 'Superior Izquierdo';
                    else if (quadrant === 'lower-left') labelElement.textContent = 'Inferior Izquierdo';
                    else if (quadrant === 'lower-right') labelElement.textContent = 'Inferior Derecho';
                    
                    quadrantElement.appendChild(labelElement);
                }
                
                quadrantElement.appendChild(teethContainer);
            } else {
                // Limpiar solo los dientes, no el label
                teethContainer.innerHTML = '';
            }
            
            teeth.forEach((toothNumber, index) => {
                // Crear estructura del diente
                const toothElement = document.createElement('div');
                toothElement.className = `tooth ${quadrant.includes('upper') ? 'upper-tooth' : 'lower-tooth'}`;
                toothElement.dataset.tooth = toothNumber;
                toothElement.style.animationDelay = `${0.1 + (index * 0.05)}s`;
                
                // Número del diente
                const numberElement = document.createElement('div');
                numberElement.className = 'tooth-number';
                numberElement.textContent = toothNumber;
                toothElement.appendChild(numberElement);
                
                // Si es cuadrante superior, primero la raíz y luego la corona
                if (quadrant.includes('upper')) {
                    // Raíz
                    const rootElement = document.createElement('div');
                    rootElement.className = 'tooth-root';
                    toothElement.appendChild(rootElement);
                    
                    // Corona
                    const crownElement = document.createElement('div');
                    crownElement.className = 'tooth-crown';
                    toothElement.appendChild(crownElement);
                } else {
                    // Corona
                    const crownElement = document.createElement('div');
                    crownElement.className = 'tooth-crown';
                    toothElement.appendChild(crownElement);
                    
                    // Raíz
                    const rootElement = document.createElement('div');
                    rootElement.className = 'tooth-root';
                    toothElement.appendChild(rootElement);
                }
                
                // Crear superficies
                const surfacesElement = document.createElement('div');
                surfacesElement.className = 'tooth-surfaces';
                
                // Superficie oclusal/incisal
                const occlusalElement = document.createElement('div');
                occlusalElement.className = 'tooth-surface surface-occlusal';
                occlusalElement.dataset.surface = 'occlusal';
                surfacesElement.appendChild(occlusalElement);
                
                // Superficie vestibular/bucal
                const buccalElement = document.createElement('div');
                buccalElement.className = 'tooth-surface surface-buccal';
                buccalElement.dataset.surface = 'buccal';
                surfacesElement.appendChild(buccalElement);
                
                // Superficie lingual/palatina
                const lingualElement = document.createElement('div');
                lingualElement.className = 'tooth-surface surface-lingual';
                lingualElement.dataset.surface = 'lingual';
                surfacesElement.appendChild(lingualElement);
                
                // Superficie mesial
                const mesialElement = document.createElement('div');
                mesialElement.className = 'tooth-surface surface-mesial';
                mesialElement.dataset.surface = 'mesial';
                surfacesElement.appendChild(mesialElement);
                
                // Superficie distal
                const distalElement = document.createElement('div');
                distalElement.className = 'tooth-surface surface-distal';
                distalElement.dataset.surface = 'distal';
                surfacesElement.appendChild(distalElement);
                
                toothElement.appendChild(surfacesElement);
                
                // AÑADIR AL CONTENEDOR DE DIENTES, NO AL CUADRANTE DIRECTAMENTE
                teethContainer.appendChild(toothElement);
                
                // Aplicar estados existentes si hay datos
                this.applyExistingStates(toothElement, toothNumber);
                
                // Añadir manejador de eventos solo si no es de solo lectura
                if (!this.readOnly) {
                    // Añadir manejador de eventos para todo el diente
                    toothElement.addEventListener('click', (e) => {
                        // Si no se hizo clic en una superficie específica, afectar todo el diente
                        if (!e.target.classList.contains('tooth-surface')) {
                            this.selectTooth(toothElement, toothNumber);
                            this.applyTool(toothElement);
                        }
                    });
                    
                    // Añadir manejadores de eventos para las superficies
                    const surfaces = toothElement.querySelectorAll('.tooth-surface');
                    surfaces.forEach(surface => {
                        surface.addEventListener('click', (e) => {
                            e.stopPropagation(); // Evitar que el evento se propague al diente completo
                            this.selectTooth(toothElement, toothNumber);
                            this.applySurfaceTool(toothElement, toothNumber, surface.dataset.surface);
                        });
                    });
                }
            });
        }
        
        // Generar resumen de intervenciones si existe el contenedor
        this.generateTeethSummary();
    }
    
    // Aplica estados existentes a un diente
    applyExistingStates(toothElement, toothNumber) {
        const strToothNumber = toothNumber.toString();
        if (this.teethData[strToothNumber]) {
            let parsedData = this.teethData[strToothNumber];
            
            // Si es un estado general del diente
            if (typeof parsedData === 'string') {
                toothElement.classList.add(parsedData);
                
                // REMOVE THIS BLOCK OR REPLACE WITH TOOLTIP
                /*
                // Add treatment label
                const treatmentLabel = document.createElement('span');
                treatmentLabel.className = 'treatment-label';
                treatmentLabel.textContent = toolNames[parsedData] || parsedData;
                toothElement.appendChild(treatmentLabel);
                */
                
                // Instead, use tooltip
                const tipText = toolNames[parsedData] || parsedData;
                toothElement.setAttribute('title', `Diente ${toothNumber}: ${tipText}`);
                toothElement.setAttribute('data-bs-toggle', 'tooltip');
                toothElement.setAttribute('data-bs-placement', 'top');
                
            } 
            // Si son estados por superficie
            else if (typeof parsedData === 'object' && parsedData !== null) {
                // Crear un texto para el tooltip que liste todas las superficies afectadas
                let tooltipText = `Diente ${toothNumber}:\n`;
                let surfacesInfo = [];
                
                for (const [surface, state] of Object.entries(parsedData)) {
                    const surfaceElement = toothElement.querySelector(`.surface-${surface}`);
                    if (surfaceElement) {
                        surfaceElement.style.backgroundColor = getToolColor(state);
                        surfaceElement.dataset.state = state;
                        
                        // Añadir tooltip a la superficie
                        const surfaceName = surfaceNames[surface] || surface;
                        const stateName = toolNames[state] || state;
                        surfaceElement.setAttribute('title', `${surfaceName}: ${stateName}`);
                        surfaceElement.setAttribute('data-bs-toggle', 'tooltip');
                        surfaceElement.setAttribute('data-bs-placement', 'top');
                        
                        // Añadir a la lista para el tooltip general del diente
                        surfacesInfo.push(`${surfaceName}: ${stateName}`);
                    }
                }
                
                // Añadir tooltip al diente completo con información de todas las superficies
                if (surfacesInfo.length > 0) {
                    tooltipText += surfacesInfo.join('\n');
                    toothElement.setAttribute('title', tooltipText);
                    toothElement.setAttribute('data-bs-toggle', 'tooltip');
                    toothElement.setAttribute('data-bs-placement', 'top');
                }
            }
        }
    }
    
    // Seleccionar un diente
    selectTooth(toothElement, toothNumber) {
        // Eliminar la clase 'selected' de todos los dientes
        document.querySelectorAll('.tooth').forEach(tooth => {
            tooth.classList.remove('selected');
        });
        
        // Añadir la clase 'selected' al diente clickeado
        toothElement.classList.add('selected');
        
        // Guardar el diente seleccionado
        this.selectedTooth = toothElement;
        
        // Mostrar información del diente si existe panel
        const toothInfoPanel = document.getElementById('tooth-info-panel');
        if (toothInfoPanel) {
            this.updateToothInfoPanel(toothNumber);
        }
    }
    
    // Aplicar herramienta al diente completo
    applyTool(toothElement) {
        if (this.readOnly) return;
        
        const toothNumber = toothElement.dataset.tooth;
        
        // Eliminar cualquier clase de estado anterior y etiquetas previas
        ['caries', 'restoration', 'extraction', 'crown', 'implant', 'bridge', 'root-canal', 'sealant', 'veneer', 'fracture', 'mobility'].forEach(cls => {
            toothElement.classList.remove(cls);
        });
        
        // Eliminar etiqueta de tratamiento previa si existe
        const oldLabel = toothElement.querySelector('.treatment-label');
        if (oldLabel) {
            oldLabel.remove();
        }
        
        // Si la herramienta es borrar, eliminar el estado
        if (this.activeTool === 'erase') {
            delete this.teethData[toothNumber];
            
            // Eliminar tooltip
            toothElement.removeAttribute('title');
            toothElement.removeAttribute('data-bs-toggle');
            
            // Eliminar tooltip si existe
            const tooltip = bootstrap.Tooltip.getInstance(toothElement);
            if (tooltip) {
                tooltip.dispose();
            }
        } else {
            // Aplicar el nuevo estado
            toothElement.classList.add(this.activeTool);
            this.teethData[toothNumber] = this.activeTool;
            
            // IMPORTANT: Choose ONE approach - either tooltip or treatment-label, not both
            // Option 1: Add tooltip (more professional and consistent with Bootstrap)
            const tipText = toolNames[this.activeTool] || this.activeTool;
            toothElement.setAttribute('title', `Diente ${toothNumber}: ${tipText}`);
            toothElement.setAttribute('data-bs-toggle', 'tooltip');
            toothElement.setAttribute('data-bs-placement', 'top');
            
            // Remove any existing tooltip and initialize a new one
            const tooltip = bootstrap.Tooltip.getInstance(toothElement);
            if (tooltip) {
                tooltip.dispose();
            }
            new bootstrap.Tooltip(toothElement);
            
            // NO LONGER CREATING TREATMENT LABELS - REMOVE THIS CODE
            // const treatmentLabel = document.createElement('span');
            // treatmentLabel.className = 'treatment-label';
            // treatmentLabel.textContent = toolNames[this.activeTool] || this.activeTool;
            // toothElement.appendChild(treatmentLabel);
        }
        
        // Eliminar cualquier estado de superficie que pueda tener el diente
        const surfaces = toothElement.querySelectorAll('.tooth-surface');
        surfaces.forEach(surface => {
            surface.style.backgroundColor = 'transparent';
            surface.dataset.state = '';
            surface.innerHTML = ''; // Eliminar cualquier etiqueta dentro
            
            // Eliminar tooltip
            surface.removeAttribute('title');
            surface.removeAttribute('data-bs-toggle');
            
            // Eliminar tooltip si existe
            const tooltip = bootstrap.Tooltip.getInstance(surface);
            if (tooltip) {
                tooltip.dispose();
            }
        });
        
        // Actualizar información del diente si existe panel
        const toothInfoPanel = document.getElementById('tooth-info-panel');
        if (toothInfoPanel) {
            this.updateToothInfoPanel(toothNumber);
        }
        
        // Actualizar campo oculto para el formulario
        this.updateHiddenField();
        
        // Notificar cambios
        this.onStateChange(this.teethData);
    }
    
    // Aplicar herramienta a una superficie específica
    applySurfaceTool(toothElement, toothNumber, surfaceName) {
        if (this.readOnly) return;
        
        const surfaceElement = toothElement.querySelector(`.surface-${surfaceName}`);
        
        if (!surfaceElement) return;
        
        // Eliminar cualquier clase de estado general del diente
        ['caries', 'restoration', 'extraction', 'crown', 'implant', 'bridge', 'root-canal', 'sealant', 'veneer', 'fracture', 'mobility'].forEach(cls => {
            toothElement.classList.remove(cls);
        });
        
        // Eliminar etiqueta de tratamiento del diente si existe
        const oldLabel = toothElement.querySelector('.treatment-label');
        if (oldLabel) {
            oldLabel.remove();
        }
        
        // Preparar objeto para guardar estados por superficie
        if (typeof this.teethData[toothNumber] !== 'object' || this.teethData[toothNumber] === null || typeof this.teethData[toothNumber] === 'string') {
            this.teethData[toothNumber] = {};
        }
        
        // Si la herramienta es borrar, eliminar estado de la superficie
        if (this.activeTool === 'erase') {
            surfaceElement.style.backgroundColor = 'transparent';
            surfaceElement.innerHTML = ''; // Eliminar cualquier etiqueta dentro
            delete this.teethData[toothNumber][surfaceName];
            
            // Eliminar tooltip
            surfaceElement.removeAttribute('title');
            surfaceElement.removeAttribute('data-bs-toggle');
            
            // Eliminar tooltip si existe
            const tooltip = bootstrap.Tooltip.getInstance(surfaceElement);
            if (tooltip) {
                tooltip.dispose();
            }
            
            // Si no quedan superficies con estado, eliminar el diente del registro
            if (Object.keys(this.teethData[toothNumber]).length === 0) {
                delete this.teethData[toothNumber];
            }
        } else {
            // Aplicar el nuevo estado a la superficie
            surfaceElement.style.backgroundColor = getToolColor(this.activeTool);
            surfaceElement.dataset.state = this.activeTool;
            this.teethData[toothNumber][surfaceName] = this.activeTool;
            
            // NO LONGER CREATING SURFACE LABELS - COMPLETELY REMOVE THIS
            // const surfaceLabel = document.createElement('span');
            // surfaceLabel.className = 'surface-label';
            // surfaceLabel.textContent = toolNames[this.activeTool].substring(0, 3);
            // surfaceElement.appendChild(surfaceLabel);
            
            // Añadir tooltip a la superficie - KEEP ONLY THIS FOR TOOLTIPS
            const surfaceDisplay = surfaceNames[surfaceName] || surfaceName;
            const stateDisplay = toolNames[this.activeTool] || this.activeTool;
            surfaceElement.setAttribute('title', `${surfaceDisplay}: ${stateDisplay}`);
            surfaceElement.setAttribute('data-bs-toggle', 'tooltip');
            surfaceElement.setAttribute('data-bs-placement', 'top');
            
            // Update tooltip if it exists
            const tooltip = bootstrap.Tooltip.getInstance(surfaceElement);
            if (tooltip) {
                tooltip.dispose();
            }
            new bootstrap.Tooltip(surfaceElement);
            
            // Actualizar tooltip del diente con todas las superficies afectadas
            this.updateToothTooltip(toothElement, toothNumber);
        }
        
        // Actualizar información del diente si existe panel
        const toothInfoPanel = document.getElementById('tooth-info-panel');
        if (toothInfoPanel) {
            this.updateToothInfoPanel(toothNumber);
        }
        
        // Actualizar campo oculto para el formulario
        this.updateHiddenField();
        
        // Notificar cambios
        this.onStateChange(this.teethData);
    }
    
    // Actualizar el tooltip del diente basado en sus superficies
    updateToothTooltip(toothElement, toothNumber) {
        if (this.teethData[toothNumber] && typeof this.teethData[toothNumber] === 'object') {
            let tooltipText = `Diente ${toothNumber}:\n`;
            let surfacesInfo = [];
            
            for (const [surface, state] of Object.entries(this.teethData[toothNumber])) {
                const surfaceName = surfaceNames[surface] || surface;
                const stateName = toolNames[state] || state;
                surfacesInfo.push(`${surfaceName}: ${stateName}`);
            }
            
            // Añadir tooltip al diente completo con información de todas las superficies
            if (surfacesInfo.length > 0) {
                tooltipText += surfacesInfo.join('\n');
                toothElement.setAttribute('title', tooltipText);
                toothElement.setAttribute('data-bs-toggle', 'tooltip');
                toothElement.setAttribute('data-bs-placement', 'top');
                
                // Actualizar tooltip si existe
                const tooltip = bootstrap.Tooltip.getInstance(toothElement);
                if (tooltip) {
                    tooltip.dispose();
                }
                new bootstrap.Tooltip(toothElement);
            }
        }
    }
    
    // Actualizar el panel de información del diente
    updateToothInfoPanel(toothNumber) {
        const infoPanel = document.getElementById('tooth-info-panel');
        if (!infoPanel) return;
        
        // Mostrar el panel
        infoPanel.style.display = 'block';
        
        const selectedToothNumber = document.getElementById('selected-tooth-number');
        const affectedSurfaces = document.getElementById('affected-surfaces');
        const toothStatus = document.getElementById('tooth-status');
        
        if (selectedToothNumber) selectedToothNumber.textContent = toothNumber;
        
        if (affectedSurfaces) {
            affectedSurfaces.innerHTML = '';
            
            const surfaceNames = {
                'occlusal': 'Oclusal',
                'buccal': 'Bucal/Vestibular',
                'lingual': 'Lingual/Palatina',
                'mesial': 'Mesial',
                'distal': 'Distal'
            };
            
            if (this.teethData[toothNumber]) {
                // Verificar si necesitamos parsear
                let parsedData = this.teethData[toothNumber];
                
                if (typeof parsedData === 'string' && parsedData.includes('{')) {
                    try {
                        parsedData = JSON.parse(parsedData);
                    } catch (e) {
                        parsedData = this.teethData[toothNumber];
                    }
                }
                
                if (typeof parsedData === 'object' && parsedData !== null) {
                    // Estados por superficie
                    for (const [surface, state] of Object.entries(parsedData)) {
                        const badge = document.createElement('span');
                        badge.className = `badge bg-${getToolColorClass(state)} me-1 mb-1`;
                        badge.innerHTML = `${surfaceNames[surface] || surface} <i class="fas fa-arrow-right ms-1"></i> ${toolNames[state] || state}`;
                        affectedSurfaces.appendChild(badge);
                    }
                    
                    if (affectedSurfaces.children.length === 0) {
                        affectedSurfaces.textContent = 'Sin afecciones en superficies';
                    }
                } else {
                    affectedSurfaces.textContent = 'Sin afecciones en superficies';
                }
            } else {
                affectedSurfaces.textContent = 'Sin afecciones en superficies';
            }
        }
        
        if (toothStatus) {
            toothStatus.innerHTML = '';
            
            if (this.teethData[toothNumber]) {
                // Verificar si necesitamos parsear
                let parsedData = this.teethData[toothNumber];
                
                if (typeof parsedData === 'string' && parsedData.includes('{')) {
                    try {
                        parsedData = JSON.parse(parsedData);
                    } catch (e) {
                        parsedData = this.teethData[toothNumber];
                    }
                }
                
                if (typeof parsedData === 'string') {
                    // Estado general del diente
                    const badge = document.createElement('span');
                    badge.className = `badge bg-${getToolColorClass(parsedData)} me-1`;
                    badge.textContent = toolNames[parsedData] || parsedData;
                    toothStatus.appendChild(badge);
                } else {
                    toothStatus.textContent = 'Normal';
                }
            } else {
                toothStatus.textContent = 'Normal';
            }
        }
    }
    
    // Actualizar campo oculto con los datos para el formulario
    updateHiddenField() {
        const container = document.getElementById('tooth-data-container');
        if (!container) return;
        
        // Limpiar contenedor
        container.innerHTML = '';
        
        // Crear campo oculto con todos los datos
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'odontogram_data';
        hiddenField.value = JSON.stringify(this.teethData);
        container.appendChild(hiddenField);
        
        // También crear campos individuales para cada diente (alternativa)
        for (const [toothNumber, data] of Object.entries(this.teethData)) {
            const toothField = document.createElement('input');
            toothField.type = 'hidden';
            toothField.name = `diente_${toothNumber}`;
            toothField.value = typeof data === 'object' ? JSON.stringify(data) : data;
            container.appendChild(toothField);
        }
    }
    
    // Generar resumen de intervenciones
    generateTeethSummary() {
        const summaryContainer = document.getElementById('teeth-summary');
        if (!summaryContainer) return;
        
        summaryContainer.innerHTML = '';
        
        // Crear estructura para agrupar por tipo de intervención
        const interventionsByType = {};
        
        // Procesar los datos para organizarlos por tipo de intervención
        for (const [toothNumber, data] of Object.entries(this.teethData)) {
            let parsedData = data;
            
            // Si es un string que parece JSON, parsearlo
            if (typeof data === 'string' && data.includes('{')) {
                try {
                    parsedData = JSON.parse(data);
                } catch (e) {
                    // Si no es JSON válido, tratarlo como string simple
                    parsedData = data;
                }
            }
            
            if (typeof parsedData === 'string') {
                // Es un estado general (afecta todo el diente)
                const interventionType = parsedData;
                const interventionName = toolNames[interventionType] || interventionType;
                
                if (!interventionsByType[interventionName]) {
                    interventionsByType[interventionName] = [];
                }
                
                interventionsByType[interventionName].push({
                    tooth: toothNumber,
                    surface: null
                });
            } else if (typeof parsedData === 'object' && parsedData !== null) {
                // Son estados por superficie
                for (const [surface, state] of Object.entries(parsedData)) {
                    const interventionType = state;
                    const interventionName = toolNames[interventionType] || interventionType;
                    
                    if (!interventionsByType[interventionName]) {
                        interventionsByType[interventionName] = [];
                    }
                    
                    interventionsByType[interventionName].push({
                        tooth: toothNumber,
                        surface: surface,
                        surfaceName: surfaceNames[surface] || surface
                    });
                }
            }
        }
        
        // Verificar si hay intervenciones
        if (Object.keys(interventionsByType).length === 0) {
            summaryContainer.innerHTML = '<div class="alert alert-info mb-0">No hay intervenciones registradas en este odontograma.</div>';
            return;
        }
        
        // Crear elementos para cada tipo de intervención
        for (const [interventionName, interventions] of Object.entries(interventionsByType)) {
            const interventionType = Object.keys(toolNames).find(key => toolNames[key] === interventionName) || interventionName;
            
            const interventionTitle = document.createElement('h6');
            interventionTitle.className = 'mb-3';
            interventionTitle.innerHTML = `<i class="fas ${getIconForIntervention(interventionType)} me-2 text-${getToolColorClass(interventionType)}"></i>${interventionName}`;
            summaryContainer.appendChild(interventionTitle);
            
            const interventionList = document.createElement('div');
            interventionList.className = 'mb-4';
            
            interventions.forEach(item => {
                const pill = document.createElement('span');
                pill.className = `tooth-info-pill bg-${getToolColorClass(interventionType)}-subtle text-${getToolColorClass(interventionType)}`;
                
                if (item.surface) {
                    pill.textContent = `Diente ${item.tooth} - ${item.surfaceName || surfaceNames[item.surface] || item.surface}`;
                } else {
                    pill.textContent = `Diente ${item.tooth}`;
                }
                
                interventionList.appendChild(pill);
            });
            
            summaryContainer.appendChild(interventionList);
        }
    }
}

// Exportar la clase para uso global
window.Odontograma = Odontograma;