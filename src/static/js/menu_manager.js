menuManager = {
    
    // Initialize menu system
    init: function() {
        if (!localStorage.getItem('vnews_menus')) {
            this.saveMenus(this.defaultMenus);
        }
    },

    // Get all menus
    getMenus: function() {
        const menus = localStorage.getItem('vnews_menus');
        return menus ? JSON.parse(menus) : this.defaultMenus;
    },

    // Get parent menus only
    getParentMenus: function() {
        const menus = this.getMenus();
        return menus.filter(menu => menu.parent_id === null).sort((a, b) => a.order - b.order);
    },

    // Get child menus by parent id
    getChildMenus: function(parentId) {
        const menus = this.getMenus();
        return menus.filter(menu => menu.parent_id === parentId).sort((a, b) => a.order - b.order);
    },

    // Get menu by id
    getMenuById: function(id) {
        const menus = this.getMenus();
        return menus.find(menu => menu.id === id);
    },

    // Save menus to localStorage
    saveMenus: function(menus) {
        localStorage.setItem('vnews_menus', JSON.stringify(menus));
    },

    // Add new menu
    addMenu: function(menuData) {
        const menus = this.getMenus();
        const newId = Math.max(...menus.map(m => m.id), 0) + 1;
        
        const newMenu = {
            id: newId,
            name: menuData.name,
            slug: menuData.slug || this.slugify(menuData.name),
            icon: menuData.icon || null,
            order: menuData.order || 999,
            visible: menuData.visible !== false,
            parent_id: menuData.parent_id || null
        };
        
        menus.push(newMenu);
        this.saveMenus(menus);
        return newMenu;
    },

    // Update menu
    updateMenu: function(id, menuData) {
        const menus = this.getMenus();
        const index = menus.findIndex(menu => menu.id === id);
        
        if (index !== -1) {
            menus[index] = {
                ...menus[index],
                ...menuData,
                id: id // Ensure id doesn't change
            };
            this.saveMenus(menus);
            return menus[index];
        }
        return null;
    },

    // Delete menu
    deleteMenu: function(id) {
        let menus = this.getMenus();
        
        // Delete child menus first
        menus = menus.filter(menu => menu.parent_id !== id);
        
        // Delete the menu itself
        menus = menus.filter(menu => menu.id !== id);
        
        this.saveMenus(menus);
        return true;
    },

    // Toggle visibility
    toggleVisibility: function(id) {
        const menus = this.getMenus();
        const menu = menus.find(m => m.id === id);
        if (menu) {
            menu.visible = !menu.visible;
            this.saveMenus(menus);
            return menu;
        }
        return null;
    },

    // Update order
    updateOrder: function(id, newOrder) {
        const menus = this.getMenus();
        const menu = menus.find(m => m.id === id);
        if (menu) {
            menu.order = newOrder;
            this.saveMenus(menus);
            return menu;
        }
        return null;
    },

    // Generate slug from name
    slugify: function(text) {
        const from = "àáäâãèéëêìíïîòóöôõùúüûñçăắằẳẵặâấầẩẫậđèéẹẻẽêếềểễệìíịỉĩòóọỏõôốồổỗộơớờởỡợùúụủũưứừửữựỳýỵỷỹ";
        const to = "aaaaaeeeeiiiioooooouuuuncaaaaaaaaaaaadeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyy";
        
        let slug = text.toLowerCase();
        
        for (let i = 0; i < from.length; i++) {
            slug = slug.replace(new RegExp(from[i], 'g'), to[i]);
        }
        
        slug = slug.replace(/[^a-z0-9 -]/g, '')
                   .replace(/\s+/g, '-')
                   .replace(/-+/g, '-')
                   .replace(/^-+/, '')
                   .replace(/-+$/, '');
        
        return slug;
    },

    // Build hierarchical menu structure
    buildMenuTree: function() {
        const menus = this.getMenus();
        const parentMenus = menus.filter(m => m.parent_id === null && m.visible)
                                  .sort((a, b) => a.order - b.order);
        
        return parentMenus.map(parent => ({
            ...parent,
            children: menus.filter(m => m.parent_id === parent.id && m.visible)
                          .sort((a, b) => a.order - b.order)
        }));
    },

    // Reset to default menus
    resetToDefault() {
        this.saveMenus(this.defaultMenus);
        return true;
    }

}