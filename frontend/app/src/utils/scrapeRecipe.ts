import axios from 'axios';
import { Recipe } from '../data/recipe_detail';

type Partial<T> = {
    [K in keyof T]?: T[K];
  };

type RecipePartial = Partial<Recipe>;

/**
 * Scrape Recipe data from a URL.
 * @param {string} url
 * @returns {RecipePartial} A Recipe object with the data.
 */
export async function scrapeRecipe(url: string): Promise<RecipePartial> {
    let recipe: RecipePartial = {};
        const response = await axios.get(url);
        const html: string = response.data;
        console.log(html);
        // #TODO: Call endpoint for scraping Recipe.
    return recipe;
}
