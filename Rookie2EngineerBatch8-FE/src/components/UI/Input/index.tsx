export interface CommonInputProps {
  /** Unique identifier for the input element. Used for accessibility and form handling */
  id?: string;

  /** Name of the input field. Used for form submission and field identification */
  name: string;

  /** Additional CSS classes to apply to the input component */
  className?: string;

  /** 
   * Width of the input field.
   * @important This prop overrides default width styling
   * @example
   * width="w-48" // Tailwind class
   * width="w-[200px]" // Arbitrary value
   *  */
  width?: string;

  /** Icon size */
  iconSize?: number
}
