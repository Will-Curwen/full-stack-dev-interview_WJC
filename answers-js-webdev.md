# Considerations for Web Application Design

## General considerations

1. Layout Stucture -
    - How is the layout controlled?
    - Can it be configured for mobile viewing? Collapsible sidebars are good for mobile viewing - if we could view webapp on work phones could this be useful on site, especially if more information is to be stored on this platform
2. State management
    - Documentation recommends using Pinia for managing global state information. This is information that needs to be shared across multiple components or pages. Using Pinia, you can create a self-contained module that stores user data, and then use this module in any component.
3. Accessibility
     - Semantic https - makes the website more accessible for screen readers, other developers and searching. USe HTML elements that clearly describe their purpose 
     - Keyboard navigation
4. Performance
     - Lazy loading - Only load parts of the application when needed. Split code into chunks and load each chunk on demand.
5. Consistency
6. User Feedback
     - Loading indicators, human readable error messages, success pop-ups


## Nuxt Specific Considerations

1. Components and modular structure
    - Can build modular systems that are accessible throughout the project without having to reimport them for every page.
    - Can break down UI into reusable components
    - Define the layout of the page in a separate file (`layouts/default.vue`) and reference the components in there. This creates a common user interface for several pages.
2. Nuxt UI
    - Provides prebuilt components
    - In this case we can use `<UHeader>, <UContainer>, <UButton>` etc. for consistency.
    - The theme can then be customised using the `nuxt.config.ts` file
3. Authentication
    - Can use an inbuilt Nuxt Auth module
    - Store user data in Pinia as mentioned above

## Steps
1. Get Nuxt!
2. Create a Nuxt project.
3. Install Nuxt Ui and add it to `nuxt.config.ts`
4. Create a layout to be shared across pages
5. Add a page
6. Run the application!